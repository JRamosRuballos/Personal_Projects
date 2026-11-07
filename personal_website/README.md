# Personal Website

Personal portfolio for Jaimny Ramos Ruballos, built with TanStack Start, React, and Tailwind CSS.

## Development

```sh
bun install
bun run dev      # http://localhost:8080
bun run build
```

## Project images

The projects section pulls from GitHub automatically (see `src/lib/projects.config.ts`).
Each project card shows an image, chosen like this:

**Projects that live in a folder** (listed in `FOLDER_PROJECTS`)

Put an image named exactly `portfolio.png` at the top level of that folder, then commit and push it:

```
Personal_Projects/
└── tic_tac_toe/
    ├── portfolio.png   <- shown on the website
    └── ...
```

- The name is case-sensitive: `portfolio.png`, not `Portfolio.PNG`, `portfolio.jpg` or `screenshot.png`.
- It must be directly inside the project folder, not in a subfolder.
- It must be pushed to GitHub, and the repository must be public. A local-only file won't show up.
- Without it, the card has no image.

**Projects that are their own repository**

These use the repository's GitHub social preview image, so `portfolio.png` is not read. To set your own, go to the repository's Settings, then General, then Social preview, and upload an image (1280x640 works best). If you don't upload one, GitHub generates a default card.

**Timing:** the site caches GitHub responses for about 2 minutes, so a new image may take a moment to appear after you push.
