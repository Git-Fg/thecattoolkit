---
name: architecting-slides
description: "Expertise in narrative structure, academic storytelling, and LaTeX Beamer presentations. Use when designing the flow of research talks and building technical slide decks with a focus on scientific rigor and narrative clarity."
allowed-tools: [Read, Write, Edit, Bash]
---

# Scientific Slides

## Overview

Expertise in narrative structure, academic storytelling, and LaTeX Beamer presentations. Use when designing the flow of research talks and building technical slide decks with a focus on scientific rigor and narrative clarity.

**CRITICAL DESIGN PHILOSOPHY**: Scientific presentations should be **NARRATIVELY COHERENT** and **RESEARCH-BACKED**. Focus on the story arc of the science.

## Quick Start

```bash
# Plan talk structure
# (Narrative planning is the first step)

# Choose a LaTeX template
# assets/beamer_template_conference.tex

# Integrate visuals from sys-multimodal
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

## Workflows

### LaTeX Beamer (Default - Recommended)

**Best for**: Mathematical content, consistent formatting, academic rigor.

1. **Choose template** from `assets/` (e.g., `beamer_template_conference.tex`)
2. **Customize theme** and colors
3. **Add content** (equations, code, algorithms)
4. **Narrative Review**: Ensure flow matches the story arc in `references/presentation_structure.md`
5. **Compile** to PDF

See `references/beamer_workflow.md` for documentation.

### Visual Presentations (Hybrid)

**Best for**: Visually stunning results, fast creation.

1. **Plan**: Create detailed narrative plan for each slide.
2. **Generate**: Use `sys-multimodal` or `canvas-design` skills for visual assets.
3. **Combine**: Assemble into PDF with `scripts/slides_to_pdf.py` (powered by `sys-multimodal` utilities).

## Reference Library

### Core Resources
- **Structure**: `references/presentation_structure.md` - Story arcs, talk types, timing
- **Design**: `references/slide_design_principles.md` - Typography, color, layout, accessibility
- **Visualization**: `references/data_visualization_slides.md` - Chart types, simplification, recreation

### Advanced Guides
- **Talk Types**: `references/talk_types_guide.md` - Conference, seminar, defense, grant, journal club specific guidance
- **Beamer**: `references/beamer_guide.md` - LaTeX themes, customization, advanced features
- **Visual Review**: `references/visual_review_workflow.md` - Validation, iteration, quality assurance

## Core Principles

1. **Narrative-Driven**: Every talk must follow a clear story arc.
2. **Research-Backed**: Use research-lookup to find 8-15 papers, cite properly.
3. **Mathematical Precision**: Use LaTeX/Beamer for complex technical content.
4. **Minimal Text**: 3-4 bullets, 4-6 words each, 24-28pt font minimum.
5. **Structural Integrity**: Clear transitions between introduction, methods, results, and discussion.

## Script Reference

### scripts/slides_to_pdf.py
Uses shared `sys-multimodal` utilities to combine images into a single PDF.
```bash
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

### scripts/pdf_to_images.py
Uses shared `sys-multimodal` utilities to convert PDF to images for review.
```bash
python scripts/pdf_to_images.py presentation.pdf slides
```

### scripts/validate_presentation.py
Validates slide count, duration, and LaTeX compilation.
```bash
python scripts/validate_presentation.py presentation.pdf --duration 15
```

## Common Pitfalls

- BAD **Lack of clear narrative arc** → GOOD **Follow established talk structures**
- BAD **Dry, text-heavy slides** → GOOD **High-quality visuals from sys-multimodal**
- BAD **Missing research context** → GOOD **Proper citations from research-lookup**
- BAD **Inconsistent LaTeX formatting** → GOOD **Standard Beamer templates**

**Remember**: A scientific talk is a story about discovery. Focus on the narrative flow as much as the data.

