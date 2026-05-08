# Color Scheme & Typography

All tokens are defined in two places:
- **Figma:** `🎨 Tokens` page → variable collections `Primitives / Colors`, `Semantic / Colors`, `Spacing & Radius`
- **Code:** `assets/css/main.css` → `:root` block at the top of the file

---

## Color System

### Primitives

These are the raw palette values. Never use them directly in components — always go through a semantic token.

#### Brand — Primary (Teal-Indigo)

Chosen for: technical precision, calm authority, not the generic startup blue.

| Token | Hex | Use |
|---|---|---|
| `--p-primary-100` | `#D4F1F4` | Light tints, badge backgrounds |
| `--p-primary-300` | `#14B5BC` | Dark mode primary |
| `--p-primary-500` | `#0D7377` | Main brand colour |
| `--p-primary-700` | `#0A5C60` | Hover state |

#### Brand — Accent (Warm Amber)

Chosen for: "playful up close" — reserved exclusively for CTAs and key interactions. Creates contrast against the teal without clashing.

| Token | Hex | Use |
|---|---|---|
| `--p-accent-100` | `#FEF2CE` | Accent tints, chip backgrounds |
| `--p-accent-500` | `#F59E0B` | Primary CTA buttons |
| `--p-accent-600` | `#D97706` | Hover state |

#### Neutral Scale (Cool Gray)

Slight blue tint reinforces the "machine / precise" brand feel.

| Token | Hex |
|---|---|
| `--p-gray-900` | `#0F1117` |
| `--p-gray-800` | `#1A1D27` |
| `--p-gray-700` | `#2D3147` |
| `--p-gray-600` | `#4A5176` |
| `--p-gray-500` | `#6B7299` |
| `--p-gray-400` | `#8F96B8` |
| `--p-gray-300` | `#BEC3D9` |
| `--p-gray-200` | `#DEE1EE` |
| `--p-gray-100` | `#ECEEF5` |
| `--p-gray-50`  | `#F4F5FA` |

#### Special Surfaces

| Token | Hex | Note |
|---|---|---|
| `--p-surface` | `#F9F7F4` | Warm off-white — prevents the "too corporate/cold" misread |
| `--p-white`   | `#ffffff` | Card surfaces in light mode |

---

### Semantic Tokens

These are what components actually use. They map to primitives and switch value between Light and Dark mode.

**Usage rule:** 70% neutrals · 20% primary · 10% accent. Accent should feel like a reward — only on CTAs and key interactions.

| Token | Light | Dark | Scope |
|---|---|---|---|
| `--bg-base` | `#F9F7F4` | `#0F1117` | Page background |
| `--bg-surface` | `#ffffff` | `#1A1D27` | Cards, navbar |
| `--bg-subtle` | `#F4F5FA` | `#1A1D27` | Alternate section backgrounds |
| `--bg-inverse` | `#D4F1F4` | `#0C2A2D` | Feature sections (About, Post Hero) — light teal in light mode, dark teal in dark mode |
| `--brand-primary` | `#0D7377` | `#14B5BC` | Brand fills, icons |
| `--brand-hover` | `#0A5C60` | `#0D7377` | Brand hover states |
| `--brand-bg` | `#D4F1F4` | `#1A1D27` | Badge/chip backgrounds |
| `--accent` | `#F59E0B` | `#F59E0B` | CTA buttons |
| `--accent-hover` | `#D97706` | `#D97706` | CTA hover |
| `--accent-bg` | `#FEF2CE` | `#1A1D27` | Accent chip backgrounds |
| `--text-primary` | `#0F1117` | `#F4F5FA` | Body text, headings |
| `--text-secondary` | `#4A5176` | `#8F96B8` | Subtitles, descriptions |
| `--text-muted` | `#6B7299` | `#6B7299` | Dates, captions, metadata |
| `--text-inverse` | `#0A5C60` | `#ffffff` | Headings/primary text on inverse backgrounds |
| `--text-inverse-muted` | `#4A5176` | `#BEC3D9` | Secondary text on inverse backgrounds |
| `--text-brand` | `#0D7377` | `#14B5BC` | Links, labels |
| `--text-accent` | `#D97706` | `#F59E0B` | Accent text |
| `--border` | `#DEE1EE` | `#2D3147` | Default borders |
| `--border-strong` | `#BEC3D9` | `#4A5176` | Emphasis borders |
| `--border-brand` | `#0D7377` | `#14B5BC` | Brand-coloured borders |

### Dark Mode

Activated automatically via `prefers-color-scheme: dark`.  
Can be overridden manually by setting `data-theme="dark"` or `data-theme="light"` on `<html>`.  
User preference is persisted to `localStorage` (key: `theme`).

---

## Typography

### Typefaces

| Role | Family | Weights | Why |
|---|---|---|---|
| **Headlines** | Space Grotesk | 400, 500, 700 | Geometric, slightly quirky — systematised without being soulless. Distinctive enough to not be generic. |
| **Body / UI** | Inter | 400, 500, 600 | Most legible sans-serif at small sizes. Invisible when it works. |
| **Code** | JetBrains Mono | 400, 500 | Signals "engineer" naturally in code blocks and experiment labels. |

Loaded via Google Fonts. Self-host if performance becomes a concern.

### Type Scale

| Style | Family | Weight | Size | Line Height | Letter Spacing |
|---|---|---|---|---|---|
| `display/hero` | Space Grotesk | Bold | 72px | 110% | −2% |
| `heading/h1` | Space Grotesk | Bold | 56px | 115% | −1.5% |
| `heading/h2` | Space Grotesk | Bold | 40px | 120% | −1% |
| `heading/h3` | Space Grotesk | Medium | 28px | 130% | −0.5% |
| `heading/h4` | Space Grotesk | Medium | 22px | 135% | 0 |
| `body/large` | Inter | Regular | 18px | 160% | 0 |
| `body/base` | Inter | Regular | 16px | 160% | 0 |
| `body/small` | Inter | Regular | 14px | 160% | 0 |
| `label/medium` | Inter | Medium | 14px | 140% | +1% |
| `label/small` | Inter | Medium | 12px | 140% | +1% |
| `ui/nav-link` | Inter | Semi Bold | 15px | 140% | 0 |
| `ui/button` | Inter | Semi Bold | 15px | 100% | +0.5% |
| `ui/caption` | Inter | Regular | 12px | 150% | 0 |
| `code/base` | JetBrains Mono | Regular | 14px | 160% | 0 |

---

## Spacing Scale

| Token | Value | CSS Variable |
|---|---|---|
| xs | 4px | `--sp-xs` |
| sm | 8px | `--sp-sm` |
| md | 16px | `--sp-md` |
| lg | 24px | `--sp-lg` |
| xl | 32px | `--sp-xl` |
| 2xl | 48px | `--sp-2xl` |
| 3xl | 64px | `--sp-3xl` |
| 4xl | 96px | `--sp-4xl` |
| 5xl | 128px | `--sp-5xl` |

## Border Radius Scale

| Token | Value | CSS Variable |
|---|---|---|
| sm | 4px | `--r-sm` |
| md | 8px | `--r-md` |
| lg | 12px | `--r-lg` |
| xl | 16px | `--r-xl` |
| 2xl | 24px | `--r-2xl` |
| full | 9999px | `--r-full` |

## Layout

| Token | Value | CSS Variable |
|---|---|---|
| Content width | 1200px | `--content-width` |
| Article width | 720px | `--article-width` |
| Section horizontal padding | 120px | `--section-pad-x` |
