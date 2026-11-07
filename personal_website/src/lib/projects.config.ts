/**
 * Project showcase curation.
 *
 * Everything here is plain text you can edit. The projects section on the home
 * page reads this file, then merges it with whatever GitHub reports live.
 *
 * The default rule is "show my real work automatically":
 *   any public repository of yours that is not a fork, not archived and actually
 *   contains code appears on the site with no edit needed.
 *
 * Use the lists below only to override that:
 *   HIDDEN            keep a repository off the site
 *   PINNED            force repositories to the front, in this order
 *   FOLDER_PROJECTS   show a folder inside a repository as its own project
 *   OVERRIDES         replace a project's title, description or tech tags
 */

export const GITHUB_USER = "JRamosRuballos";

/** Repositories that never appear on the site. */
export const HIDDEN: string[] = [
  // Empty placeholders — nothing to look at yet.
  "testing",
  "sample_stuff",
  "cart_a_la_carte",
  "SOSC_13320_Project",
  "2026_hack_for_accessibility",
  // Forks of other people's work.
  "lab-1",
  "fullstack-hy2020.github.io",
  // Small exercises.
  "git-tutorial",
  // Its folders are listed individually in FOLDER_PROJECTS below,
  // so the umbrella repository is not shown as a card of its own.
  "Personal_Projects",
];

/** Repositories pinned to the front of the grid, in this order. */
export const PINNED: string[] = [];

/**
 * Projects that live in a folder of a repository instead of their own repository.
 * Add one line per folder: `repo` is the repository, `path` the folder inside it.
 */
export const FOLDER_PROJECTS: {
  repo: string;
  path: string;
  title?: string;
  description?: string;
}[] = [
  {
    repo: "Personal_Projects",
    path: "face_recognition",
    title: "Face Recognition Tool",
    description:
      "Live face recognition built on OpenCV and DeepFace. Rewritten to accept multiple reference images per person and adapted to run on macOS.",
  },
  {
    repo: "Personal_Projects",
    path: "weather_app",
    title: "Weather Desktop App",
    description:
      "PyQt5 desktop app that pulls live conditions for any US city from the OpenWeatherMap API, with explicit handling for bad input, offline clients and upstream server failures.",
  },
  {
    repo: "Personal_Projects",
    path: "personal_website",
    title: "Personal Site (first build)",
    description:
      "Hand-written personal site: a C core, a Python layer and a browser front end, deployed through Cloudflare Workers.",
  },
  {
    repo: "Personal_Projects",
    path: "number_guesser",
    title: "Number Guesser",
    description: "Terminal number-guessing game written as a warm-up exercise.",
  },
];

/**
 * Replace a project's copy. Key is the repository name, or `repo/path` for a
 * folder project. Any field you leave out falls back to what GitHub says.
 */
export const OVERRIDES: Record<
  string,
  { title?: string; description?: string; tags?: string[] }
> = {};

/** Folders that are coursework rather than portfolio pieces. */
export const HIDDEN_FOLDERS: string[] = ["Personal_Projects/college_assignments"];

/** How many tech tags a card shows at most. */
export const MAX_TAGS = 4;
