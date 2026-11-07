import {
  FOLDER_PROJECTS,
  GITHUB_USER,
  HIDDEN,
  HIDDEN_FOLDERS,
  MAX_TAGS,
  OVERRIDES,
} from "./projects.config";
import { newestProjectsFirst } from "./project-updates";
import type { Project, ProjectBundle, ProjectTag } from "./projects.types";

const PUBLIC_API = "https://api.github.com";
const CACHE_TTL_MS = 2 * 60 * 1000;
const REQUEST_TIMEOUT_MS = 6000;

const LANGUAGE_COLORS: Record<string, string> = {
  Python: "#3572A5",
  HTML: "#e34c26",
  CSS: "#563d7c",
  JavaScript: "#f1e05a",
  TypeScript: "#3178c6",
  C: "#555555",
  "C++": "#f34b7d",
  Java: "#b07219",
  Go: "#00ADD8",
  "Go Template": "#00ADD8",
  R: "#358a56",
  SQL: "#e38c00",
  Shell: "#89e051",
  PowerShell: "#012456",
  "Jupyter Notebook": "#DA5B0B",
  Ruby: "#701516",
  Rust: "#dea584",
  Swift: "#F05138",
  Kotlin: "#A97BFF",
  Vue: "#41b883",
  Svelte: "#ff3e00",
};

const EXTENSION_LANGUAGES: Record<string, string> = {
  ".py": "Python",
  ".c": "C",
  ".h": "C",
  ".cpp": "C++",
  ".cc": "C++",
  ".hpp": "C++",
  ".js": "JavaScript",
  ".mjs": "JavaScript",
  ".jsx": "JavaScript",
  ".ts": "TypeScript",
  ".tsx": "TypeScript",
  ".html": "HTML",
  ".htm": "HTML",
  ".css": "CSS",
  ".ipynb": "Jupyter Notebook",
  ".r": "R",
  ".sql": "SQL",
  ".sh": "Shell",
  ".ps1": "PowerShell",
  ".go": "Go",
  ".java": "Java",
  ".rb": "Ruby",
  ".rs": "Rust",
};

type RawRepo = {
  name: string;
  full_name: string;
  html_url: string;
  description: string | null;
  private?: boolean;
  visibility?: string;
  fork?: boolean;
  archived?: boolean;
  size?: number;
  language?: string | null;
  homepage?: string | null;
  stargazers_count?: number;
  forks_count?: number;
  pushed_at?: string | null;
  topics?: string[];
};

type RawContent = { name: string; type: string; download_url: string | null };

/**
 * One GitHub read against GitHub's public, unauthenticated API.
 * Returns null on any failure so the caller can degrade instead of throwing.
 */
async function github(
  path: string,
  params: Record<string, string | number> = {},
): Promise<unknown | null> {
  const query = new URLSearchParams(
    Object.entries(params).map(([key, value]) => [key, String(value)]),
  ).toString();
  const suffix = query ? `?${query}` : "";

  // GitHub rejects requests without a User-Agent (Workers don't send one by default).
  const headers: Record<string, string> = {
    Accept: "application/vnd.github+json",
    "User-Agent": "jaimny-personal-website",
  };
  // Optional: raises the rate limit from 60/hr (shared per Cloudflare IP) to 5000/hr.
  const token = typeof process !== "undefined" ? process.env?.GITHUB_TOKEN : undefined;
  if (token) headers.Authorization = `Bearer ${token}`;

  const target = `${PUBLIC_API}${path}${suffix}`;
  try {
    const response = await fetch(target, {
      headers,
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });
    if (!response.ok) {
      console.error(`GitHub read failed [${response.status}] ${path}`);
      return null;
    }
    return (await response.json()) as unknown;
  } catch (error) {
    console.error(`GitHub read threw for ${path}`, error);
    return null;
  }
}

function tag(name: string): ProjectTag {
  return { name, color: LANGUAGE_COLORS[name] ?? null };
}

/** Top languages of a repository, by bytes of code. */
async function repoTags(fullName: string): Promise<ProjectTag[]> {
  const languages = await github(`/repos/${fullName}/languages`);
  if (!languages || typeof languages !== "object") return [];
  return Object.entries(languages as Record<string, number>)
    .sort((a, b) => b[1] - a[1])
    .slice(0, MAX_TAGS)
    .map(([name]) => tag(name));
}

/** Latest commit on the default branch, optionally scoped to a project folder. */
async function lastCommitDate(fullName: string, path?: string): Promise<string | null> {
  const commits = await github(`/repos/${fullName}/commits`, {
    per_page: 1,
    ...(path ? { path } : {}),
  });
  if (!Array.isArray(commits)) return null;
  const date = (commits[0] as { commit?: { committer?: { date?: string } } } | undefined)?.commit?.committer?.date;
  return date && Number.isFinite(Date.parse(date)) ? date : null;
}

/** Read languages and the optional portfolio.png preview in one folder read. */
async function folderDetails(
  repo: string,
  path: string,
): Promise<{ tags: ProjectTag[]; image: string | null }> {
  const encodedPath = path.split("/").map(encodeURIComponent).join("/");
  const contents = await github(`/repos/${GITHUB_USER}/${encodeURIComponent(repo)}/contents/${encodedPath}`);
  if (!Array.isArray(contents)) return { tags: [], image: null };
  const seen = new Set<string>();
  let image: string | null = null;
  for (const entry of contents as RawContent[]) {
    if (entry.type !== "file") continue;
    if (entry.name === "portfolio.png" && entry.download_url?.startsWith("https://raw.githubusercontent.com/")) {
      image = entry.download_url;
    }
    const dot = entry.name.lastIndexOf(".");
    if (dot <= 0) continue;
    const language = EXTENSION_LANGUAGES[entry.name.slice(dot).toLowerCase()];
    if (language) seen.add(language);
  }
  return { tags: [...seen].slice(0, MAX_TAGS).map(tag), image };
}

/** A repository is worth a card only if it holds code and is yours to show. */
export function isShowable(repo: RawRepo): boolean {
  if (repo.private === true || (repo.visibility && repo.visibility !== "public")) {
    return false;
  }
  if (repo.fork || repo.archived) return false;
  if (HIDDEN.includes(repo.name)) return false;
  return Boolean(repo.language) || (repo.size ?? 0) > 0;
}

function toRepoProject(repo: RawRepo, tags: ProjectTag[], updated: string | null): Project {
  const override = OVERRIDES[repo.name] ?? {};
  return {
    slug: repo.full_name,
    title: override.title ?? repo.name.replace(/[-_]+/g, " "),
    description: override.description ?? repo.description ?? "No description yet.",
    url: repo.html_url,
    path: null,
    image: `https://opengraph.githubassets.com/1/${repo.full_name}`,
    tags: override.tags?.length ? override.tags.map(tag) : tags,
    stars: repo.stargazers_count ?? 0,
    forks: repo.forks_count ?? 0,
    updated,
    kind: "repo",
  };
}

function toFolderProject(
  entry: (typeof FOLDER_PROJECTS)[number],
  tags: ProjectTag[],
  image: string | null,
  updated: string | null,
): Project {
  const slug = `${GITHUB_USER}/${entry.repo}/${entry.path}`;
  const override = OVERRIDES[`${entry.repo}/${entry.path}`] ?? {};
  return {
    slug,
    title: override.title ?? entry.title ?? entry.path.replace(/[-_]+/g, " "),
    description:
      override.description ?? entry.description ?? "No description yet.",
    url: `https://github.com/${GITHUB_USER}/${entry.repo}/tree/main/${entry.path}`,
    path: `${entry.repo}/${entry.path}`,
    image,
    tags: override.tags?.length ? override.tags.map(tag) : tags,
    stars: 0,
    forks: 0,
    updated,
    kind: "folder",
  };
}

let cache: { at: number; value: ProjectBundle } | null = null;

export async function loadProjects(): Promise<ProjectBundle> {
  if (cache && Date.now() - cache.at < CACHE_TTL_MS) return cache.value;

  const raw = await github(`/users/${GITHUB_USER}/repos`, {
    per_page: 100,
    sort: "pushed",
    direction: "desc",
  });

  if (!Array.isArray(raw)) {
    const value: ProjectBundle = {
      user: GITHUB_USER,
      profileUrl: `https://github.com/${GITHUB_USER}`,
      repoUrl: `https://github.com/${GITHUB_USER}?tab=repositories`,
      projects: [],
      syncedAt: Date.now(),
      error: "GitHub could not be reached.",
    };
    // Do not cache a failure for long: the next visitor should retry.
    cache = { at: Date.now() - CACHE_TTL_MS + 60_000, value };
    return value;
  }

  const showable = (raw as RawRepo[]).filter(isShowable);
  // Hidden umbrella repositories can supply folders, but private ones cannot.
  const publicRepos = new Set(
    (raw as RawRepo[])
      .filter((repo) => repo.private !== true && (!repo.visibility || repo.visibility === "public"))
      .map((repo) => repo.name),
  );
  const folders = FOLDER_PROJECTS.filter(
    (entry) => publicRepos.has(entry.repo) && !HIDDEN_FOLDERS.includes(`${entry.repo}/${entry.path}`),
  );

  const [repoTagsList, folderDetailsList, repoDates, folderDates] = await Promise.all([
    Promise.all(showable.map((repo) => repoTags(repo.full_name))),
    Promise.all(folders.map((entry) => folderDetails(entry.repo, entry.path))),
    Promise.all(showable.map((repo) => lastCommitDate(repo.full_name))),
    Promise.all(folders.map((entry) => lastCommitDate(`${GITHUB_USER}/${entry.repo}`, entry.path))),
  ]);

  const repoProjects = showable
    .map((repo, index) => toRepoProject(repo, repoTagsList[index] ?? [], repoDates[index] ?? null));

  const folderProjects = folders.map((entry, index) => {
    const details = folderDetailsList[index];
    return toFolderProject(entry, details?.tags ?? [], details?.image ?? null, folderDates[index] ?? null);
  });

  const value: ProjectBundle = {
    user: GITHUB_USER,
    profileUrl: `https://github.com/${GITHUB_USER}`,
    repoUrl: `https://github.com/${GITHUB_USER}?tab=repositories`,
    projects: newestProjectsFirst([...folderProjects, ...repoProjects]),
    syncedAt: Date.now(),
    error: null,
  };
  cache = { at: Date.now(), value };
  return value;
}
