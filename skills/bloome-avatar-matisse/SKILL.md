---
name: bloome-avatar-matisse
description: Generate Bloome agent avatars in the established Matisse-like silhouette style distilled from the Bloome avatar set. Use when an agent needs to create or regenerate a Bloome profile avatar, relationship avatar, symbolic avatar, or vibe avatar that should match this exact visual language rather than a generic illustration, anime portrait, 3D icon, or realistic character.
version: 1
---

# Bloome Avatar Matisse

## Overview

Use this skill when generating square Bloome avatars that must match the existing house style.
The target look is flat, bold, iconic, and slightly surreal: one dark silhouette on one solid background, minimal interior detail, no shading, no realism.

## Core Style

- Use a square canvas.
- Use exactly one solid background color and one solid dark foreground silhouette.
- Keep the drawing flat and graphic. No gradients, textures, lighting, bevels, gloss, 3D, photorealism, or painterly brushwork.
- Build the subject from large cut-paper-like shapes with soft irregular edges.
- Keep interior detail sparse: eyes, nose bridges, lips, hair cutouts, leaf sprigs, stars, hearts, or simple symbolic marks only.
- Keep the composition centered and legible at avatar size.
- Prefer strong negative space and a single memorable shape over many details.
- Let the image feel human, playful, and slightly strange, but not cute-cartoon or mascot-like.

## Allowed Motifs

- Single portrait heads
- Paired or group figures
- Birds, leaves, stars, suns, moons, hearts, flowers, abstract limbs
- Human-like silhouettes with simplified faces
- Emotional or relational symbols between figures

## Forbidden Traits

- Realistic skin, hair, clothing, or facial rendering
- Camera framing language such as depth of field, cinematic lighting, bokeh, lens blur
- Detailed anatomy, fingers, wrinkles, eyelashes, teeth
- Multi-color characters or outlined sticker style
- UI chrome, typography, logos, badges, speech bubbles
- Watercolor, oil painting, clay, plastic, 3D mascot, emoji, anime, kawaii, Pixar-like output

## Palette Rules

- Prefer high-contrast pairings.
- Background should be warm or cool but muted enough to feel art-directed, not neon-generic.
- Foreground should usually be near-black or very dark charcoal.
- Use one background color only.
- Use the established Bloome avatar background palette first. Preferred background colors:
  - `cobalt blue` `#2556B6`
  - `coral red` `#F36440`
  - `soft sky` `#ADC8E6`
  - `ochre` `#F49F6A`
  - `amber yellow` `#FFD15C`
  - `olive green` `#BAC78D`
  - `purple` `#7A68BF`
- If a prompt does not specify a background, choose from that list instead of inventing a new one.
- Reserve cream/off-white only when explicitly needed; the default palette above is the house set.
- Recommended foreground:
  - black
  - near-black brown
  - deep charcoal

## Avatar Modes

Choose one mode before prompting:

- Portrait: one face or bust, iconic profile/front hybrid, sparse facial cutouts.
- Together: two figures or heads with a small relational symbol between them.
- Element: one bird, plant, star, moon, or abstract symbol.
- Vibe: simplified dancing or gesturing bodies with strong rhythm.

## Generation Workflow

1. Decide the avatar mode: `portrait`, `together`, `element`, or `vibe`.
2. Choose one background color from the house palette and one dark silhouette color.
3. Write a prompt that describes only large-shape composition, silhouette language, and 1-2 symbolic details.
4. Explicitly ban realism, gradients, outlines, text, and extra colors.
5. Generate 3-4 variants when possible, then keep the most legible one.
6. Prefer the variant that still reads clearly at small size.

## Prompt Formula

Use this structure:

`Square Bloome agent avatar in a flat Matisse-like cut-paper silhouette style. [subject]. One solid [background color] background. One solid near-black silhouette. Minimal interior cutouts only. Bold organic shapes, slightly surreal, iconic, centered composition, no text, no border, no gradients, no shading, no realism, no 3D.`

## Prompt Recipes

Read [references/prompt-recipes.md](references/prompt-recipes.md) for ready-to-use prompt patterns for each avatar mode.

## Output Requirements

- Export as `png`.
- Keep the canvas square.
- Keep the subject centered with breathing room near the edges.
- Do not add captions or labels into the image.
- If the model keeps adding texture or extra colors, simplify the prompt and restate `flat two-color silhouette`.

## Review Checklist

Reject and regenerate if any of these happen:

- more than two meaningful colors
- visible shading or lighting
- facial detail becomes realistic
- composition feels busy or small
- symbols are too tiny to read
- avatar looks like a poster, sticker sheet, or logo lockup instead of a square avatar
- output feels generic midjourney-art instead of cut-paper silhouette
