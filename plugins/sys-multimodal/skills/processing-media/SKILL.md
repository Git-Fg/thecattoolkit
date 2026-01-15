---
name: processing-media
description: "Handles video editing, ffmpeg processing, and visual analysis. Use when transforming raw footage into polished output or analyzing visual content."
allowed-tools: [Read, Write, Edit, Glob, Bash(ffmpeg:*), Bash(ffprobe:*)]
---

# Video Editing Protocol



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
1.  **Analyze**: Use processing-media skill to understand video content (specs, visual content).
2.  **Translate**: Convert natural language command to edit parameters (EDL/FFMPEG).
3.  **Edit**: Apply changes using ffmpeg.
4.  **Verify**: Validate output quality programmatically (Self-Verification).



## Quality Standards
- No artifacts or quality degradation
- Clear dialogue, balanced audio levels
- Narrative flow enhancement
- Accurate intent interpretation

## Reference Library
- `references/edl-generation.md`: How to structure complex edits.
- `references/frame-analysis.md`: Visual inspection protocols.
- `references/ffmpeg-recipes.md`: (Common commands - *to be populated*)
