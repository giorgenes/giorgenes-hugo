# giorgenes.github.io

Personal site for [Giorgenes](https://giorgenes.github.io) — polymath software engineer & designer.

Built with [Hugo](https://gohugo.io). Content authored in [Obsidian](https://obsidian.md) and synced at build time.

## Stack

- **Hugo** — static site generator
- **Obsidian** — content authoring (notes with `public: true` are published)
- **GitHub Pages** — hosting
- **GitHub Actions** — CI/CD

## Local development

```bash
hugo server
```

## Sync content from Obsidian

```bash
cp .env.example .env   # set OBSIDIAN_PATH
python scripts/sync-obsidian.py
```

## Deploy

Pushes to `main` trigger the GitHub Actions workflow which builds and deploys to GitHub Pages automatically.
