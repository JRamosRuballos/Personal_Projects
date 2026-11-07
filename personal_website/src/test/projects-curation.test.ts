import { describe, expect, it } from "vitest";

import { isShowable } from "@/lib/github.server";
import {
  FOLDER_PROJECTS,
  GITHUB_USER,
  HIDDEN,
  HIDDEN_FOLDERS,
} from "@/lib/projects.config";
import type { ProjectBundle } from "@/lib/projects.types";

/** Minimal stand-in for a GitHub repository payload. */
function repo(overrides: Record<string, unknown> = {}) {
  return {
    name: "fresh-repo",
    full_name: `${GITHUB_USER}/fresh-repo`,
    html_url: `https://github.com/${GITHUB_USER}/fresh-repo`,
    description: "Something real.",
    private: false,
    visibility: "public",
    fork: false,
    archived: false,
    size: 120,
    language: "Python",
    ...overrides,
  } as never;
}

describe("Project showcase curation", () => {
  it("shows a brand new public repository with code, with no config edit", () => {
    expect(isShowable(repo())).toBe(true);
  });

  it("keeps every private repository off the public site", () => {
    expect(isShowable(repo({ private: true, visibility: "private" }))).toBe(false);
    expect(isShowable(repo({ visibility: "internal" }))).toBe(false);
  });

  it("keeps forks and archived repositories off the site", () => {
    expect(isShowable(repo({ fork: true }))).toBe(false);
    expect(isShowable(repo({ archived: true }))).toBe(false);
  });

  it("keeps repositories with nothing in them off the site", () => {
    expect(isShowable(repo({ size: 0, language: null }))).toBe(false);
  });

  it("keeps the repositories listed as hidden off the site", () => {
    for (const name of HIDDEN) {
      expect(isShowable(repo({ name }))).toBe(false);
    }
  });

  it("hides the placeholder and fork repositories from this account", () => {
    for (const name of [
      "testing",
      "sample_stuff",
      "cart_a_la_carte",
      "SOSC_13320_Project",
      "2026_hack_for_accessibility",
      "lab-1",
      "fullstack-hy2020.github.io",
      "git-tutorial",
      "Personal_Projects",
    ]) {
      expect(HIDDEN).toContain(name);
    }
  });

  it("lists each folder project as its own project with copy of its own", () => {
    expect(FOLDER_PROJECTS.length).toBeGreaterThan(0);
    for (const entry of FOLDER_PROJECTS) {
      expect(entry.repo).toBeTruthy();
      expect(entry.path).toBeTruthy();
      expect(entry.title).toBeTruthy();
      expect(entry.description).toBeTruthy();
      expect(HIDDEN_FOLDERS).not.toContain(`${entry.repo}/${entry.path}`);
    }
  });

  it("keeps coursework folders out of the showcase", () => {
    expect(HIDDEN_FOLDERS).toContain("Personal_Projects/college_assignments");
  });
});

describe("GitHub failure handling", () => {
  it("hands the page an empty list plus an error instead of throwing", () => {
    const bundle: ProjectBundle = {
      user: GITHUB_USER,
      profileUrl: `https://github.com/${GITHUB_USER}`,
      repoUrl: `https://github.com/${GITHUB_USER}?tab=repositories`,
      projects: [],
      syncedAt: Date.now(),
      error: "GitHub could not be reached.",
    };

    expect(bundle.projects).toEqual([]);
    expect(bundle.error).toBe("GitHub could not be reached.");
  });
});
