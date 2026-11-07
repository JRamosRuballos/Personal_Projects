import { afterEach, describe, expect, it, vi } from "vitest";
import { newestProjectsFirst, relativeProjectUpdate } from "@/lib/project-updates";
import type { Project } from "@/lib/projects.types";
import { GITHUB_USER } from "@/lib/projects.config";

afterEach(() => { vi.unstubAllGlobals(); vi.resetModules(); });

describe("Project updates", () => {
  it("formats a commit three weeks ago using relative dates", () => {
    expect(relativeProjectUpdate("2026-10-17T15:00:00Z", Date.parse("2026-11-07T15:00:00Z"))).toBe("3 weeks ago");
  });

  it("sorts folders and repositories together newest first with undated projects last", () => {
    const projects = [
      { slug: "old-folder", kind: "folder", updated: "2026-10-01T00:00:00Z" },
      { slug: "undated", kind: "repo", updated: null },
      { slug: "new-repo", kind: "repo", updated: "2026-11-01T00:00:00Z" },
    ] as Project[];
    expect(newestProjectsFirst(projects).map(p => p.slug)).toEqual(["new-repo", "old-folder", "undated"]);
    expect(projects[0]?.slug).toBe("old-folder");
  });

  it("reads actual commit dates for repositories and path-scoped folders, preserving tags", async () => {
    const fetchMock = vi.fn(async (input: string) => {
      const url = new URL(input);
      const payload = url.pathname.includes("/users/") ? [
        { name: "Personal_Projects", private: false, visibility: "public" },
        { name: "new-repo", full_name: `${GITHUB_USER}/new-repo`, html_url: "https://github.com/example", language: "Python", pushed_at: "2026-01-01T00:00:00Z" },
      ] : url.pathname.endsWith("/commits") ? [{ commit: { committer: { date: url.searchParams.has("path") ? "2026-10-17T15:00:00Z" : "2026-11-07T15:00:00Z" } } }]
        : url.pathname.endsWith("/languages") ? { Python: 100 }
        : [{ name: "app.py", type: "file", download_url: null }];
      return new Response(JSON.stringify(payload));
    });
    vi.stubGlobal("fetch", fetchMock);
    const { loadProjects } = await import("@/lib/github.server");
    const bundle = await loadProjects();
    expect(bundle.projects[0]?.slug).toBe(`${GITHUB_USER}/new-repo`);
    expect(bundle.projects[0]?.updated).toBe("2026-11-07T15:00:00Z");
    const folder = bundle.projects.find(p => p.path === "Personal_Projects/face_recognition");
    expect(folder?.updated).toBe("2026-10-17T15:00:00Z");
    expect(folder?.tags.map(t => t.name)).toEqual(["Python"]);
    expect(fetchMock.mock.calls.some(([url]) => new URL(url).searchParams.get("path") === "face_recognition")).toBe(true);
  });
});