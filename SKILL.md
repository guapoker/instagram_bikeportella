---
name: instagram-content
description: Create Instagram content for Bike Portella — carousels, product posts, promotions, reels covers. Use this skill whenever the user asks to create Instagram posts, social media content, carousel slides, product announcements, promotional graphics, or reels thumbnails for the bike shop. Also trigger when asked to generate visual content for @bikeportella, create posts about bicycles/e-bikes/accessories/parts, or design any social media visual following Bike Portella's brand. Covers the full pipeline from idea to final PNG using Gemini image generation + HTML/CSS templates + Playwright rendering.
---

# Instagram Content Creation — Bike Portella

## Overview

This skill creates Instagram-ready PNG content for @bikeportella using a three-stage pipeline:

```
Roteiro → Gemini gera imagem → Template HTML + textos → Playwright renderiza PNG
```

The Content Agent creates drafts only. Nothing is posted without Marcel's approval.

## Pipeline — 5 Steps

### Step 1: Define Idea and Script

Before generating anything, define:

1. **Post type** — which template to use (see Template Selection below)
2. **Objective** — educate, sell, engage, inform
3. **All text content** — title, subtitle, body, CTA, price, specs
4. **Caption draft** with hashtags

For carousels, script slide by slide:
- Slide 1 (Hook): Eye-catching title + icon or striking image
- Slides 2-N (Content): One point per slide, image + short text
- Final Slide (CTA): Call to action + contact info + logo

**Anti-repetition check:** Read `memory/` to verify recent themes. Do not repeat topics posted in the last 30 days.

### Step 2: Generate Base Image with Gemini

Use Gemini Flash 2.5 to generate the base photo/illustration for each slide or post.

**Prompt guidelines:**
- Be specific about framing, angle, and style
- Include "product photography" or "technical illustration" as appropriate
- Specify "clean background" or "white background" for products
- Never ask for text in the image — text goes in the HTML template
- Specify lighting and angle when relevant

**Good prompt examples:**

Product (bicycle):
```
Professional product photography of an electric bicycle, matte black frame,
side view, centered, clean white background, studio lighting,
high detail on mechanical components, no text, no watermark
```

Educational (mechanics):
```
Close-up technical photograph of hands adjusting a bicycle rear derailleur,
workshop environment, warm lighting, shallow depth of field,
focus on the derailleur mechanism, no text overlay
```

Part/accessory:
```
Product photography of a bicycle chain on dark gray surface,
dramatic side lighting, metallic reflections, macro detail,
minimalist composition, no text, no watermark
```

Save generated images to `outputs/images/` with descriptive names:
```
outputs/images/evibe-urbam-side-view.png
outputs/images/derailleur-adjustment-closeup.png
```

### Step 3: Build HTML Template

Read the appropriate template from `templates/` directory in this skill. Each template is a complete HTML file with the correct dimensions, brand colors, and layout.

**Available templates** — read the file before starting:

| Template File | Format | Use Case |
|--------------|--------|----------|
| `templates/carousel-hook.html` | 1080×1350 | First slide of educational carousel |
| `templates/carousel-step.html` | 1080×1350 | Middle slides with step-by-step content |
| `templates/carousel-cta.html` | 1080×1350 | Final slide with call to action |
| `templates/product-bike.html` | 1080×1350 | Bicycle highlight with specs and price |
| `templates/product-accessory.html` | 1080×1080 | Helmets, gloves, lights, bags |
| `templates/product-part.html` | 1080×1080 | Chains, derailleurs, tires, brake pads |
| `templates/promo.html` | 1080×1350 | Discounts, sales, seasonal promotions |
| `templates/reels-cover.html` | 1080×1920 | Reels thumbnail for grid |

Copy the template, replace placeholder content (titles, images, prices, specs) with actual content, and save to `outputs/html/`.

For carousels, create one HTML per slide:
```
outputs/html/carousel-corrente-slide-01.html
outputs/html/carousel-corrente-slide-02.html
outputs/html/carousel-corrente-slide-03.html
```

**Inserting the Gemini image into the template:**
```html
<img src="./images/nome-da-imagem.png"
     style="width: 100%; height: 400px; object-fit: cover;" />
```

### Step 4: Render with Playwright

Use the render script at `scripts/render.py` to convert HTML to PNG.

**Single post:**
```bash
python3 scripts/render.py outputs/html/template.html outputs/post-final.png 1080 1350
```

**Full carousel:**
```bash
python3 scripts/render.py outputs/html/carousel-corrente-slide-01.html outputs/carousel-corrente-01.png 1080 1350
python3 scripts/render.py outputs/html/carousel-corrente-slide-02.html outputs/carousel-corrente-02.png 1080 1350
```

**Format dimensions reference:**
- Carousel / Product bike / Promo: `1080 1350` (4:5)
- Accessory / Part: `1080 1080` (1:1)
- Reels cover / Story: `1080 1920` (9:16)

If Playwright is not installed:
```bash
pip install playwright --break-system-packages
playwright install chromium
```

### Step 5: Review and Deliver

1. Visually check each rendered PNG
2. Save finals in `outputs/` with standard naming:
   ```
   YYYY-MM-DD-type-description-slideNN.png
   2026-03-01-carousel-manutencao-corrente-slide01.png
   ```
3. Create caption file alongside:
   ```
   2026-03-01-carousel-manutencao-corrente-legenda.md
   ```
4. **DO NOT post** — everything is a draft until Marcel approves
5. Notify that content is ready for review

---

## Template Selection Guide

Choose template based on what's being communicated:

**Educational / How-to content** → Carousel (hook + steps + CTA)
- Bike maintenance tips, "how to" guides, common mistakes
- 5-8 slides: dark hook, white content slides, dark CTA
- Use: `carousel-hook.html` + `carousel-step.html` × N + `carousel-cta.html`

**Bicycle product** → Product Bike
- New arrivals, featured bikes, e-bike highlights
- Dark background, specs bar, price with installments, red CTA bar
- Use: `product-bike.html`

**Accessory** → Product Accessory
- Helmets, gloves, glasses, bags, lights
- White/light background, clean product photo, top brand bar
- Use: `product-accessory.html`

**Mechanical part** → Product Part
- Chains, derailleurs, brake pads, tires, tubes
- Dark technical background with grid pattern, industrial feel
- Use: `product-part.html`

**Sale / Discount** → Promo
- Black Friday, seasonal, clearance, weekly deals
- Full red background, bold percentage, urgency elements
- Use: `promo.html`

**Reels / Video** → Reels Cover
- Thumbnail for Reels in the grid feed
- Vertical 9:16, play icon, bold title
- Use: `reels-cover.html`

---

## Brand Standards — Bike Portella

### Color Palette (Caloi)

```css
--red: #E30613;           /* Primary — CTAs, highlights, badges */
--red-dark: #B8050F;      /* Hover states, gradients */
--black: #1A1A1A;         /* Dark backgrounds, text on light */
--white: #FFFFFF;         /* Light backgrounds, text on dark */
--silver: #C0C0C0;        /* Secondary text, borders */
--silver-light: #E8E8E8;  /* Neutral light backgrounds */
--silver-dark: #8A8A8A;   /* Labels, metadata */
--gray: #2D2D2D;          /* Intermediate backgrounds */
--gray-mid: #404040;      /* Subtle borders, separators */
```

### Typography
- **Headings:** Helvetica Neue Bold / Arial Bold (fallback)
- **Body:** Helvetica Neue Regular / Arial (fallback)
- **Labels/tags:** Uppercase, letter-spacing 1-3px, font-weight 700
- **Prices:** Font-weight 800, red color

### Logo
- File: `LOGO_2025.pdf` (in workspace)
- Present on every slide/post
- Default position: bottom center or bottom left
- Text fallback: "BIKE PORTELLA" letter-spacing 3px, silver
- Optional subtext: "DESDE 1975"

### Rules
- Never distort the logo
- Red ONLY for highlights and CTAs, never as background for long text
- Predominant backgrounds: black or white (high contrast)
- Product images always on clean backgrounds

---

## Instagram Format Reference (2026)

| Content Type | Recommended Format | Ratio | Notes |
|-------------|-------------------|-------|-------|
| Feed carousel | 1080×1350 | 4:5 | Maximum vertical space in feed |
| Feed post (large item) | 1080×1350 | 4:5 | Bikes, premium products |
| Feed post (small item) | 1080×1080 | 1:1 | Accessories, parts |
| Story | 1080×1920 | 9:16 | Full screen vertical |
| Reels | 1080×1920 | 9:16 | Full screen vertical |
| Reels cover (grid) | 1080×1920 | 9:16 | Shows as cropped in grid |

---

## Folder Structure

```
workspace-content/
├── outputs/
│   ├── images/         ← Gemini-generated images
│   ├── html/           ← Assembled HTML templates
│   ├── *.png           ← Final rendered PNGs
│   └── *-legenda.md    ← Captions and hashtags
├── templates/          ← Reusable HTML base templates (from this skill)
├── scripts/            ← Render script (from this skill)
└── memory/             ← Editorial history and calendar
```

---

## Quality Checklist

Before delivering any content for approval:

- [ ] Correct format and dimensions for the post type
- [ ] Color palette respected (red, black, white, silver)
- [ ] Logo present (image or text fallback)
- [ ] No spelling errors in text
- [ ] Gemini image at adequate quality
- [ ] Clear CTA on last slide (carousel) or in the post
- [ ] Caption drafted with hashtags
- [ ] Topic not repeated in last 30 days (check memory/)
- [ ] File saved in outputs/ with standard naming
- [ ] No post scheduled or published without Marcel's OK
