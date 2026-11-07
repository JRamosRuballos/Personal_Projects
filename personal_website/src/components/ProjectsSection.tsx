import { useMemo, useState } from "react";
import { queryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { Github, Star } from "lucide-react";

import { getProjects } from "@/lib/projects.functions";
import { relativeProjectUpdate } from "@/lib/project-updates";
import type { Project, ProjectTag } from "@/lib/projects.types";
import { SectionLabel } from "@/components/SectionLabel";

export const projectsQueryOptions = queryOptions({
  queryKey: ["projects"],
  queryFn: () => getProjects(),
  staleTime: 5 * 60 * 1000,
});

/** Non-code work that belongs on the page but has no repository. */
const OFF_GITHUB = [
  {
    title: "First / Last Mile Analysis",
    when: "Mar 2025",
    kind: "Geospatial data science · R",
    body: "Proposed optimal Divvy bike-share station placements across Chicago by clustering CTA bus stops where arrivals run 5+ minutes off schedule.",
  },
  {
    title: "Prism × BCG Case Competition",
    when: "Feb 2026",
    kind: "Strategy",
    body: "Go-to-market proposal expanding a fantasy-sports travel agency into Asian and European markets, plus fashion and film verticals.",
  },
];

function Preview({ project }: { project: Project }) {
  const [broken, setBroken] = useState(false);

  if (project.image && !broken) {
    return (
      <img
        src={project.image}
        alt=""
        aria-hidden="true"
        loading="lazy"
        decoding="async"
        onError={() => setBroken(true)}
        className="h-full w-full object-cover object-top transition-transform duration-500 group-hover:scale-[1.03]"
      />
    );
  }

  // GitHub has no render for this project (or the image failed): draw one from
  // the theme so the card never shows a hole.
  return (
    <div className="relative h-full w-full overflow-hidden bg-accent">
      <div
        aria-hidden="true"
        className="absolute inset-0"
        style={{
          backgroundImage:
            "radial-gradient(circle at 1px 1px, var(--color-border) 1px, transparent 0)",
          backgroundSize: "14px 14px",
        }}
      />
      <div aria-hidden="true" className="absolute inset-x-0 bottom-0 h-1 bg-primary/70" />
      <div className="relative flex h-full flex-col justify-between p-5">
        <span className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
          {project.path ?? project.slug}
        </span>
        <span className="font-display text-4xl leading-none text-accent-foreground/80">
          {project.tags[0]?.name ?? "Code"}
        </span>
      </div>
    </div>
  );
}

function TagList({ tags }: { tags: ProjectTag[] }) {
  if (!tags.length) return null;
  return (
    <ul className="flex flex-wrap gap-2">
      {tags.map((t) => (
        <li
          key={t.name}
          className="flex items-center gap-1.5 rounded-sm bg-secondary px-2 py-1 font-mono text-xs text-secondary-foreground"
        >
          {t.color && (
            <span
              aria-hidden="true"
              className="h-2 w-2 rounded-full"
              style={{ backgroundColor: t.color }}
            />
          )}
          {t.name}
        </li>
      ))}
    </ul>
  );
}

function Card({ project, now }: { project: Project; now: number }) {
  const updated = relativeProjectUpdate(project.updated, now);

  return (
    <article className="group flex flex-col overflow-hidden rounded-sm border border-border bg-card transition-colors hover:bg-accent">
      <a
        href={project.url}
        target="_blank"
        rel="noreferrer"
        className="flex h-full flex-col"
      >
        <div className="aspect-[2/1] overflow-hidden border-b border-border bg-secondary">
          <Preview project={project} />
        </div>
        <div className="flex flex-1 flex-col p-6">
          <h3 className="font-display text-2xl leading-snug group-hover:text-primary">
            {project.title}
          </h3>
          <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
            {project.description}
          </p>
          <div className="mt-auto pt-5">
            <TagList tags={project.tags} />
            <p className="mt-4 text-xs text-muted-foreground">
              {updated ? <time dateTime={project.updated ?? undefined}>Updated {updated}</time> : "Update date unavailable"}
            </p>
            <div className="mt-4 flex items-center justify-between font-mono text-xs uppercase tracking-widest text-muted-foreground">
              <span className="flex items-center gap-3">
                {project.stars > 0 && (
                  <span className="flex items-center gap-1">
                    <Star className="h-3 w-3" aria-hidden="true" />
                    {project.stars}
                  </span>
                )}
              </span>
              <span className="flex items-center gap-1 text-primary">
                <Github className="h-3.5 w-3.5" aria-hidden="true" />
                Code
              </span>
            </div>
          </div>
        </div>
      </a>
    </article>
  );
}

export function ProjectsSkeleton() {
  return (
    <section id="projects" className="scroll-mt-24 py-24">
      <SectionLabel n="02">Projects</SectionLabel>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="h-80 animate-pulse rounded-sm border border-border bg-secondary"
          />
        ))}
      </div>
    </section>
  );
}

export function ProjectsSection() {
  const { data } = useSuspenseQuery(projectsQueryOptions);
  const [language, setLanguage] = useState<string | null>(null);

  const languages = useMemo(() => {
    const counts = new Map<string, number>();
    for (const project of data.projects) {
      for (const tag of project.tags) {
        counts.set(tag.name, (counts.get(tag.name) ?? 0) + 1);
      }
    }
    return [...counts.entries()]
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .map(([name]) => name);
  }, [data.projects]);

  const shown = language
    ? data.projects.filter((p) => p.tags.some((t) => t.name === language))
    : data.projects;

  return (
    <section id="projects" className="scroll-mt-24 py-24">
      <SectionLabel n="02">Projects</SectionLabel>

      <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <p className="max-w-xl text-sm leading-relaxed text-muted-foreground">
          {data.error
            ? "GitHub is not responding right now — these are the projects I keep in sync with it."
            : "Pulled live from my GitHub, so anything I push shows up here without me touching this site."}
        </p>
        <a
          href={data.profileUrl}
          target="_blank"
          rel="noreferrer"
          className="link-underline flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-primary"
        >
          <Github className="h-4 w-4" aria-hidden="true" />
          github.com/{data.user}
        </a>
      </div>

      {languages.length > 1 && (
        <div className="mb-8 flex flex-wrap gap-2" role="group" aria-label="Filter projects by language">
          <button
            type="button"
            onClick={() => setLanguage(null)}
            aria-pressed={language === null}
            className={`rounded-full border px-3 py-1 font-mono text-xs transition-colors ${
              language === null
                ? "border-primary bg-primary text-primary-foreground"
                : "border-border hover:border-primary hover:text-foreground"
            }`}
          >
            All
          </button>
          {languages.map((name) => (
            <button
              key={name}
              type="button"
              onClick={() => setLanguage(name === language ? null : name)}
              aria-pressed={language === name}
              className={`rounded-full border px-3 py-1 font-mono text-xs transition-colors ${
                language === name
                  ? "border-primary bg-primary text-primary-foreground"
                  : "border-border hover:border-primary hover:text-foreground"
              }`}
            >
              {name}
            </button>
          ))}
        </div>
      )}

      {shown.length ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {shown.map((project) => (
            <Card key={project.slug} project={project} now={data.syncedAt} />
          ))}
        </div>
      ) : (
        <p className="rounded-sm border border-dashed border-border p-8 text-center text-sm text-muted-foreground">
          No projects in {language ?? "this filter"} right now.
        </p>
      )}

      <div className="mt-10 grid gap-px overflow-hidden rounded-sm border border-border bg-border md:grid-cols-2">
        {OFF_GITHUB.map((p) => (
          <article key={p.title} className="bg-card p-6">
            <div className="flex justify-between font-mono text-xs uppercase tracking-widest text-muted-foreground">
              <span>{p.kind}</span>
              <span>{p.when}</span>
            </div>
            <h3 className="mt-4 font-display text-xl">{p.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{p.body}</p>
          </article>
        ))}
      </div>

      {!data.error && (
        <p className="mt-6 font-mono text-xs text-muted-foreground">
          Synced from GitHub · {format(new Date(data.syncedAt), "MMM d, yyyy")}
        </p>
      )}
    </section>
  );
}
