import { afterEach, describe, expect, it, vi } from "vitest";
import { FOLDER_PROJECTS, GITHUB_USER } from "@/lib/projects.config";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.resetModules();
});

async function loadWith(contents: unknown, isPrivate = false) {
  const fetchMock = vi.fn(async (input: string) => {
    const payload = input.includes(`/users/${GITHUB_USER}/repos`)
      ? [{ name: "Personal_Projects", private: isPrivate, visibility: isPrivate ? "private" : "public", size: 100, language: "Python" }]
      : input.includes("/commits") ? [] : contents;
    return new Response(JSON.stringify(payload), { status: 200 });
  });
  vi.stubGlobal("fetch", fetchMock);
  const { loadProjects } = await import("@/lib/github.server");
  return { bundle: await loadProjects(), fetchMock };
}

describe("Automatic folder project images", () => {
  it("uses portfolio.png directly in each folder and preserves language tags", async () => {
    const image = `https://raw.githubusercontent.com/${GITHUB_USER}/Personal_Projects/main/face_recognition/portfolio.png`;
    const { bundle, fetchMock } = await loadWith([
      { name: "portfolio.png", type: "file", download_url: image },
      { name: "app.py", type: "file", download_url: null },
    ]);
    expect(bundle.projects).toHaveLength(FOLDER_PROJECTS.length);
    for (const project of bundle.projects) {
      expect(project.image).toBe(image);
      expect(project.tags.map((tag) => tag.name)).toEqual(["Python"]);
    }
    expect(fetchMock).toHaveBeenCalledTimes(1 + 2 * FOLDER_PROJECTS.length);
  });

  it("keeps the existing fallback when portfolio.png is absent", async () => {
    const { bundle } = await loadWith([{ name: "app.py", type: "file", download_url: null }]);
    expect(bundle.projects).toHaveLength(FOLDER_PROJECTS.length);
    expect(bundle.projects.every((project) => project.image === null)).toBe(true);
  });

  it("requires the exact filename and a file rather than a directory", async () => {
    const { bundle } = await loadWith([
      { name: "Portfolio.png", type: "file", download_url: "https://raw.githubusercontent.com/example/other.png" },
      { name: "portfolio.png", type: "dir", download_url: null },
    ]);
    expect(bundle.projects).toHaveLength(FOLDER_PROJECTS.length);
    expect(bundle.projects.every((project) => project.image === null)).toBe(true);
  });

  it("does not expose or request folder images from a private repository", async () => {
    const { bundle, fetchMock } = await loadWith([], true);
    expect(bundle.projects).toEqual([]);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("keeps the fallback if the folder read fails", async () => {
    const { bundle } = await loadWith(null);
    expect(bundle.projects).toHaveLength(FOLDER_PROJECTS.length);
    expect(bundle.projects.every((project) => project.image === null)).toBe(true);
  });
});