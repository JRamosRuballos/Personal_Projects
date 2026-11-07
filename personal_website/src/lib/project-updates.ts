import { differenceInWeeks, formatDistance, isValid, parseISO } from "date-fns";
import type { Project } from "./projects.types";

export function relativeProjectUpdate(updated: string | null, now: number): string | null {
  if (!updated) return null;
  const date = parseISO(updated);
  if (!isValid(date)) return null;
  const weeks = differenceInWeeks(now, date);
  if (weeks >= 1 && weeks < 4) return `${weeks} ${weeks === 1 ? "week" : "weeks"} ago`;
  return formatDistance(date, now, { addSuffix: true });
}

export function newestProjectsFirst(projects: Project[]): Project[] {
  const timestamp = (date: string | null) => {
    const value = date ? Date.parse(date) : NaN;
    return Number.isFinite(value) ? value : -Infinity;
  };
  return [...projects].sort((a, b) => {
    const first = timestamp(a.updated);
    const second = timestamp(b.updated);
    return first === second ? a.slug.localeCompare(b.slug) : first > second ? -1 : 1;
  });
}