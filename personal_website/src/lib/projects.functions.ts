import { createServerFn } from "@tanstack/react-start";
import { loadProjects } from "./github.server";
import type { ProjectBundle } from "./projects.types";

/**
 * Public, read-only list of the projects shown on the portfolio.
 * Returns an empty list plus an error string instead of throwing, so the page
 * still renders when GitHub is slow or unavailable.
 */
export const getProjects = createServerFn({ method: "GET" }).handler(
  async (): Promise<ProjectBundle> => loadProjects(),
);
