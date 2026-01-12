---
name: scientific-slides
description: "Provides slide structure, design templates, timing guidance, and visual validation. Use when building slide decks and presentations for research talks. Works with PowerPoint and LaTeX Beamer."
allowed-tools: [Read, Write, Edit, Bash]
---

# Scientific Slides

## Overview

Generate research presentations using Nano Banana Pro (Visuals) or Beamer (LaTeX).

**CRITICAL DESIGN PHILOSOPHY**: Scientific presentations should be **VISUALLY ENGAGING** and **RESEARCH-BACKED**. Avoid dry, text-heavy slides.

## Quick Start

```bash
# Generate visual
python scripts/generate_slide_image.py "Title slide: Quantum Computing" -o slide.png

# Full slide with formatting
python scripts/generate_slide_image.py "Title slide: 'Machine Learning'. Speaker: K-Dense. FORMATTING GOAL: Dark blue background, white text, gold accents, minimal design." -o slides/01.png

# Attach previous slide for consistency
python scripts/generate_slide_image.py "Slide titled 'Why ML Matters'. CITATIONS: (Smith et al., 2024). FORMATTING GOAL: Match attached slide style exactly." -o slides/02.png --attach slides/01.png

# Combine to PDF
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

## Workflows

### PDF Slides (Default - Recommended)

**Best for**: Visually stunning results, fast creation, non-technical audiences

1. **Plan**: Create detailed plan for each slide
2. **Generate**: Use `generate_slide_image.py` with consistent formatting
3. **Combine**: Assemble into PDF with `slides_to_pdf.py`

**CRITICAL: Formatting Consistency Protocol**
- Define formatting goal at start (colors, typography, style)
- Attach previous slide using `--attach` for visual continuity
- Include citations directly in prompts
- Default author: "K-Dense"

See `references/pdf_workflow.md` for detailed guide.

### PowerPoint

Use Nano Banana Pro to generate visuals, then build PPTX with text.

1. **Generate visuals**: `python scripts/generate_slide_image.py "diagram" -o fig.png --visual-only`
2. **Build PPTX**: Use PPTX skill's `html2pptx` workflow
3. **Add text**: Include generated visuals with separate text

See `references/pptx_workflow.md` for complete guide.

### LaTeX Beamer

**Best for**: Mathematical content, consistent formatting

1. Choose template from `assets/` (e.g., `beamer_template_conference.tex`)
2. Customize theme and colors
3. Add content (equations, code, algorithms)
4. Compile to PDF

See `references/beamer_workflow.md` for documentation.

## Reference Library

### Core Resources
- **Design**: `references/slide_design_principles.md` - Typography, color, layout, accessibility
- **Structure**: `references/presentation_structure.md` - Story arcs, talk types, timing
- **Visualization**: `references/data_visualization_slides.md` - Chart types, simplification, recreation

### Advanced Guides
- **Talk Types**: `references/talk_types_guide.md` - Conference, seminar, defense, grant, journal club specific guidance
- **Beamer**: `references/beamer_guide.md` - LaTeX themes, customization, advanced features
- **Visual Review**: `references/visual_review_workflow.md` - Validation, iteration, quality assurance

### Assets
- `assets/beamer_template_conference.tex`: 15-minute conference talk
- `assets/beamer_template_seminar.tex`: 45-minute academic seminar
- `assets/beamer_template_defense.tex`: Dissertation defense
- **Design Guide**: `references/powerpoint_design_guide.md`
- **Timing**: `assets/timing_guidelines.md`

## Core Principles

1. **Visual-First**: Every slide needs strong visual element (figure, image, diagram)
2. **Research-Backed**: Use research-lookup to find 8-15 papers, cite properly
3. **Modern Aesthetics**: Contemporary color palette, not default themes
4. **Minimal Text**: 3-4 bullets, 4-6 words each, 24-28pt font
5. **High Contrast**: 7:1 ratio for professional appearance
6. **White Space**: 40-50% of slide empty

## Script Reference

### generate_slide_image.py
```bash
# Full slide
python scripts/generate_slide_image.py "slide description" -o output.png

# Visual only
python scripts/generate_slide_image.py "visual description" -o output.png --visual-only

# With attachments
python scripts/generate_slide_image.py "Create slide about this chart" -o slide.png --attach chart.png
```

### slides_to_pdf.py
```bash
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

### validate_presentation.py
```bash
python scripts/validate_presentation.py presentation.pdf --duration 15
```

## Integration

**Research Lookup**: Use for finding background literature, citations, comparison studies, supporting evidence, and question preparation.

**PPTX Skill**: Use for PowerPoint creation with `html2pptx` workflow and template editing.

**Scientific Schematics**: Use for complex technical diagrams and publication-quality figures.

## Common Pitfalls

- ❌ **Dry, text-heavy slides** → ✅ **High-quality visuals dominate**
- ❌ **Generic default themes** → ✅ **Modern color palettes**
- ❌ **Missing research context** → ✅ **Proper citations from research-lookup**
- ❌ **Small fonts** → ✅ **24-28pt body text minimum**

**Remember**: Boring presentations = forgotten science. Make slides visually memorable while maintaining scientific rigor.
