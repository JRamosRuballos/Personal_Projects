import { createFileRoute } from "@tanstack/react-router";
import { Suspense } from "react";

import portraitUrl from "@/assets/portrait.jpg";
import resumeUrl from "@/assets/resume.pdf";
const portrait = { url: portraitUrl };
const resume = { url: resumeUrl };
import { SectionLabel } from "@/components/SectionLabel";
import {
  ProjectsSection,
  ProjectsSkeleton,
  projectsQueryOptions,
} from "@/components/ProjectsSection";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Jaimny Ramos Ruballos — Software, Data & ML Engineer" },
      {
        name: "description",
        content:
          "Portfolio of Jaimny Ramos Ruballos, UChicago B.S./M.S. Computer Science — software engineering, data engineering, data science and machine learning.",
      },
      { property: "og:title", content: "Jaimny Ramos Ruballos — Portfolio" },
      {
        property: "og:description",
        content: "Software, data engineering, data science and machine learning work by Jaimny Ramos Ruballos.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
  loader: ({ context }) =>
    context.queryClient.ensureQueryData(projectsQueryOptions),
});

const EMAIL = "jaimnyramosruballos@gmail.com";
const LINKEDIN = "https://www.linkedin.com/in/jaimny-ramos-ruballos/";
const GITHUB = "https://github.com/JRamosRuballos";

const focus = ["Software Engineering", "Data Engineering", "Data Science", "Machine Learning"];

const stats = [
  { n: "1.8M", l: "healthcare NPIs matched with ML" },
  { n: "95%", l: "Random Forest accuracy" },
  { n: "95%", l: "less reporting time at Wayfair" },
  { n: "96K+", l: "LinkedIn profiles linked" },
];

const experience = [
  {
    org: "Wayfair",
    role: "Operations Analyst Intern",
    place: "Boston, MA",
    when: "Jun – Aug 2026",
    tags: ["BigQuery", "SQL", "Data Studio"],
    points: [
      "Engineered a BigQuery + Data Studio dashboard measuring employee efficiency across 12 fulfillment centers, automating manual reporting and cutting metric reporting time by 95%.",
      "Maintained SQL logic across 4 dashboards as warehouse technology evolved, partnering with warehouse systems engineers on data accuracy.",
      "Delivered workflow recommendations across 3 processes after an on-site visit to the Georgia fulfillment center.",
    ],
  },
  {
    org: "Alpha Sophia",
    role: "Data Science / Data Engineer Intern",
    place: "Remote",
    when: "Jun – Aug 2025",
    tags: ["Python", "scikit-learn", "Entity resolution"],
    points: [
      "Built ML-based matching logic grouping 1.8M healthcare organization NPIs into sites of care, reaching a 34.6% match rate.",
      "Trained a 95%-accurate Random Forest classifier on engineered string-similarity and geospatial-proximity features.",
    ],
  },
  {
    org: "UChicago Computer Science",
    role: "Academic Grader",
    place: "Chicago, IL",
    when: "Sep 2025 – Jun 2026",
    tags: ["Discrete Math", "Intro CS II"],
    points: [
      "Graded for 85 students in MPCS 50103 (Discrete Mathematics) and 267+ students in CMSC 14200 (Intro to Computer Science II).",
    ],
  },
  {
    org: "Alpha Sophia",
    role: "Data Science Intern",
    place: "Remote",
    when: "Jul – Aug 2024",
    tags: ["pandas", "recordlinkage"],
    points: [
      "Matched 96,000+ LinkedIn healthcare profiles to an internal provider database using pandas and recordlinkage.",
    ],
  },
];

const skills = [
  { k: "Languages", v: ["Python", "C", "SQL", "R"] },
  { k: "Data & ML", v: ["pandas", "NumPy", "scikit-learn", "recordlinkage", "Jupyter"] },
  { k: "Platforms", v: ["Google BigQuery", "Data Studio", "Git"] },
  {
    k: "Coursework",
    v: [
      "Machine Learning",
      "Adversarial ML",
      "Database Systems",
      "Systems Programming",
      "Computer Security",
      "Statistical Models",
      "Data Science I & II",
    ],
  },
];

function Index() {
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-20 border-b border-border bg-background/85 backdrop-blur">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <a href="#top" className="font-display text-2xl">
            Jaimny R. R.
          </a>
          <div className="hidden gap-8 font-mono text-xs uppercase tracking-widest text-muted-foreground md:flex">
            <a href="#work" className="link-underline hover:text-foreground">Work</a>
            <a href="#projects" className="link-underline hover:text-foreground">Projects</a>
            <a href="#skills" className="link-underline hover:text-foreground">Skills</a>
            <a href="#contact" className="link-underline hover:text-foreground">Contact</a>
          </div>
          <a
            href={resume.url}
            target="_blank"
            rel="noreferrer"
            className="rounded-sm bg-foreground px-4 py-2 font-mono text-xs uppercase tracking-widest text-background transition-colors hover:bg-primary"
          >
            Resume
          </a>
        </nav>
      </header>

      <main id="top" className="mx-auto max-w-6xl px-6">
        {/* Intro */}
        <section className="grid items-center gap-12 py-20 md:grid-cols-[1.4fr_1fr] md:py-28">
          <div className="animate-rise">
            <p className="mb-6 font-mono text-xs uppercase tracking-[0.25em] text-primary">
              CS @ UChicago · B.S./M.S. ’27 · Chicago, IL
            </p>
            <h1 className="font-display text-6xl leading-[0.95] md:text-8xl">
              Jaimny <br />
              <em className="text-primary">Ramos Ruballos</em>
            </h1>
            <p className="mt-8 max-w-xl text-lg leading-relaxed text-muted-foreground">
              I build data pipelines, matching models and dashboards that turn messy, real-world
              records into decisions — from 1.8M healthcare organizations to a dozen fulfillment
              centers.
            </p>
            <ul className="mt-8 flex flex-wrap gap-2">
              {focus.map((f) => (
                <li key={f} className="rounded-full border border-border px-3 py-1 text-sm">
                  {f}
                </li>
              ))}
            </ul>
            <div className="mt-10 flex flex-wrap gap-4">
              <a
                href={`mailto:${EMAIL}`}
                className="rounded-sm bg-primary px-6 py-3 font-medium text-primary-foreground transition-opacity hover:opacity-90"
              >
                Get in touch
              </a>
              <a
                href={resume.url}
                target="_blank"
                rel="noreferrer"
                className="rounded-sm border border-foreground px-6 py-3 font-medium transition-colors hover:bg-foreground hover:text-background"
              >
                View Resume
              </a>
            </div>
          </div>
          <div className="animate-rise relative mx-auto w-full max-w-sm [animation-delay:150ms]">
            <div className="absolute -inset-3 translate-x-4 translate-y-4 rounded-sm bg-accent" />
            <img
              src={portrait.url}
              alt="Portrait of Jaimny Ramos Ruballos"
              className="relative aspect-[4/5] w-full rounded-sm object-cover object-[50%_35%]"
            />
          </div>
        </section>

        {/* Stats */}
        <section className="grid grid-cols-2 border-y border-border md:grid-cols-4">
          {stats.map((s, i) => (
            <div key={i} className="border-border p-6 [&:not(:last-child)]:md:border-r">
              <div className="font-display text-5xl text-primary">{s.n}</div>
              <div className="mt-2 text-sm text-muted-foreground">{s.l}</div>
            </div>
          ))}
        </section>

        {/* Experience */}
        <section id="work" className="scroll-mt-24 py-24">
          <SectionLabel n="01">Experience</SectionLabel>
          <div className="space-y-12">
            {experience.map((e, i) => (
              <article key={i} className="grid gap-4 md:grid-cols-[220px_1fr]">
                <div className="font-mono text-xs uppercase tracking-widest text-muted-foreground">
                  <div>{e.when}</div>
                  <div className="mt-1">{e.place}</div>
                </div>
                <div>
                  <h3 className="text-xl font-semibold">
                    {e.role} <span className="font-display text-2xl font-normal italic text-primary">· {e.org}</span>
                  </h3>
                  <ul className="mt-3 space-y-2 leading-relaxed text-muted-foreground">
                    {e.points.map((p, j) => (
                      <li key={j} className="relative pl-5 before:absolute before:left-0 before:top-3 before:h-px before:w-3 before:bg-primary">
                        {p}
                      </li>
                    ))}
                  </ul>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {e.tags.map((t) => (
                      <span key={t} className="rounded-sm bg-secondary px-2 py-1 font-mono text-xs">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>

        {/* Projects */}
        <Suspense fallback={<ProjectsSkeleton />}>
          <ProjectsSection />
        </Suspense>

        {/* Skills + education */}
        <section id="skills" className="scroll-mt-24 py-24">
          <SectionLabel n="03">Skills & education</SectionLabel>
          <div className="grid gap-12 md:grid-cols-2">
            <dl className="space-y-6">
              {skills.map((s) => (
                <div key={s.k}>
                  <dt className="mb-2 font-mono text-xs uppercase tracking-widest text-primary">{s.k}</dt>
                  <dd className="flex flex-wrap gap-2">
                    {s.v.map((v) => (
                      <span key={v} className="rounded-full border border-border px-3 py-1 text-sm">
                        {v}
                      </span>
                    ))}
                  </dd>
                </div>
              ))}
            </dl>
            <div className="rounded-sm border border-border bg-card p-8">
              <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground">
                Sep 2023 – Jun 2027
              </p>
              <h3 className="mt-3 font-display text-3xl">The University of Chicago</h3>
              <p className="mt-1 text-muted-foreground">B.S. & M.S. in Computer Science (3+1 program)</p>
              <div className="mt-6 space-y-3 text-sm">
                <p><span className="font-semibold">Honors:</span> The Gates Scholarship, QuestBridge, Odyssey Scholar</p>
                <p><span className="font-semibold">Involvement:</span> Data Science Society (former Technical Workshop Co-Leader — SQL, R, ML), WiCyS, Student Health Advisory Board</p>
                <p><span className="font-semibold">Community:</span> Spanish–English translator, Chicago Street Medicine</p>
              </div>
            </div>
          </div>
        </section>

        {/* Contact */}
        <section id="contact" className="scroll-mt-24 border-t border-border py-24 text-center">
          <p className="font-mono text-xs uppercase tracking-[0.25em] text-primary">Open to new-grad & internship roles</p>
          <h2 className="mx-auto mt-6 max-w-3xl font-display text-5xl leading-tight md:text-7xl">
            Let’s build something <em className="text-primary">data-driven</em>.
          </h2>
          <a href={`mailto:${EMAIL}`} className="link-underline mt-10 inline-block text-lg md:text-2xl">
            {EMAIL}
          </a>
          <div className="mt-8 flex justify-center gap-8 font-mono text-xs uppercase tracking-widest">
            <a href={LINKEDIN} target="_blank" rel="noreferrer" className="link-underline">LinkedIn</a>
            <a href={GITHUB} target="_blank" rel="noreferrer" className="link-underline">GitHub</a>
            <a href={resume.url} target="_blank" rel="noreferrer" className="link-underline">Resume PDF</a>
          </div>
        </section>
      </main>

      <footer className="border-t border-border py-8 text-center font-mono text-xs text-muted-foreground">
        © 2026 Jaimny Ramos Ruballos · Chicago, IL
      </footer>
    </div>
  );
}
