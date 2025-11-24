# UmbraTrace

UmbraTrace is a dark, professional OSINT exploration UI built with SvelteKit, TypeScript, Vite, and TailwindCSS. It ships with mock intelligence APIs, advanced filtering, and export-ready PDF reports powered by pdfmake.

## Getting started

```bash
npm install
npm run dev -- --open
```

Production build:

```bash
npm run build
npm run preview
```

## Architecture

- **SvelteKit + Vite** for SSR-first rendering with client interactivity.
- **TailwindCSS** with a custom shadow palette (obsidian/onyx/neon).
- **@tanstack/svelte-query** handles async search revalidation and caching.
- **Global stores** (`src/stores`) manage theme, filters, and recent searches with localStorage persistence.
- **Mock API** lives at `src/routes/api/search/+server.ts`, reading from `src/lib/mock-data.ts` to simulate realistic OSINT responses with confidence scoring.
- **PDF exports** use `src/lib/pdf-templates.ts` for full-report and single-record exports (pdfmake with canvas/SVG embeds and SHA-256 integrity footer).
- **Components** include accessible search, skeleton loading, JSON modal, theme toggle, and export buttons.
- **Styling** is centralized in `src/styles/globals.css`; adjust color tokens in `tailwind.config.cjs` to rebrand.

## PDF generation details

The pdfmake templates generate a cover page with the UmbraTrace SVG logo, executive summary, evidence tables, bar charts rendered from the Canvas API, and a social graph SVG. A SHA-256 hash of the content is added to the footer for integrity. The `exportPdf` helper dynamically loads pdfmake to keep the bundle lean.

## Ethics and legal reminder

Only run UmbraTrace on identities you are authorized to research. The project uses mock data and read-only analysis but always respect privacy laws, platform terms, and consent requirements.
