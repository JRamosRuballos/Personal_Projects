/**
 * Shapes shared by the server that reads GitHub and the section that renders it.
 * Kept in its own client-safe module so components never import a *.server file.
 */

export type ProjectTag = { name: string; color: string | null };

export type Project = {
  slug: string;
  title: string;
  description: string;
  url: string;
  /** Folder inside a monorepo, when the project is one. Null for whole repos. */
  path: string | null;
  /** GitHub's own preview render, or null when there is none. */
  image: string | null;
  tags: ProjectTag[];
  stars: number;
  forks: number;
  updated: string | null;
  kind: "repo" | "folder";
};

export type ProjectBundle = {
  user: string;
  profileUrl: string;
  repoUrl: string;
  projects: Project[];
  syncedAt: number;
  error: string | null;
};
