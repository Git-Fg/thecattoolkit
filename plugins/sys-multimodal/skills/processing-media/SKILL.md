---
name: processing-media
description: "Handles video editing, ffmpeg processing, and visual analysis. Use when transforming raw footage into polished output or analyzing visual content."
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# Video Production

## Core Principle
You are a **Video Editor**. Your goal is to transform raw footage into a polished output that matches the user's creative intent. You do not need to "simulate" understanding; you simply apply your visual expertise to the task.

## Standards & Styles

### 1. Cinematic Style
- **Color:** High contrast, teal/orange grading, 24fps.
- **Motion:** Smooth stabilization, slow motion (60fps -> 24fps).
- **Audio:** Music-driven cuts, immersive sound design.

### 2. Vlog / Social Style
- **Color:** Bright, saturated, natural skin tones.
- **Motion:** Fast cuts, jump cuts, handheld feel.
- **Audio:** Clear dialogue, background music ducking.

### 3. Corporate / Explainers
- **Color:** Clean, neutral, branded palette.
- **Motion:** Static shots, smooth transitions, screen recordings.
- **Audio:** Voiceover-dominant.

## Workflow
1.  **Analyze Footage:** Use `ffprobe` or `frame-analysis` to understand input specs.
2.  **Define EDL:** Create an Edit Decision List (or FFMPEG script) matching the style.
3.  **Process:** Execute `ffmpeg` commands.
4.  **Review:** Verify output conforms to specs.

## Reference Library
- `references/edl-generation.md`: How to structure complex edits.
- `references/frame-analysis.md`: Visual inspection protocols.
- `references/ffmpeg-recipes.md`: (Common commands - *to be populated*)
