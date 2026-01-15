---
name: architecting-slides
description: "Expertise in narrative structure, academic storytelling, and LaTeX Beamer presentations. Use when designing the flow of research talks and building technical slide decks with a focus on scientific rigor and narrative clarity."
allowed-tools: [Read, Write, Edit, Bash]
---

# Architecting Slides Protocol

## Overview



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

### Base Templates
- **Structure**: [Presentation Structure](references/presentation_structure.md) - Story arcs, talk types, timing
- **Design**: [Slide Design Principles](references/slide_design_principles.md) - Typography, color, layout, accessibility
- **Visualization**: [Data Visualization](references/data_visualization_slides.md) - Chart types, simplification, recreation

### Advanced Guides
- **Talk Types**: [Talk Types Guide](references/talk_types_guide.md) - Conference, seminar, defense, grant, journal club specific guidance
- **Beamer**: [Beamer Guide](references/beamer_guide.md) - LaTeX themes, customization, advanced features
- **Visual Review**: [Visual Review Workflow](references/visual_review_workflow.md) - Validation, iteration, quality assurance



