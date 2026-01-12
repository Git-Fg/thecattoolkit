# PDF Workflow Guide

Generate visually stunning presentations using Nano Banana Pro to create complete slide images, then combine into PDF.

## Why PDF Workflow?

**Advantages**:
- Most visually impressive results
- Fast creation (describe and generate)
- No design skills required
- Consistent, professional appearance
- Perfect for general audiences

**Best for**: Conference talks, business presentations, general scientific talks, pitch presentations

## Step-by-Step Process

### Step 1: Plan Each Slide

Create a detailed plan for your presentation:

```markdown
# Presentation Plan: Introduction to Machine Learning

## Slide 1: Title Slide
- Title: "Machine Learning: From Theory to Practice"
- Subtitle: "AI Conference 2025"
- Speaker: Dr. Jane Smith, University of XYZ
- Visual: Modern abstract neural network background

## Slide 2: Introduction
- Title: "Why Machine Learning Matters"
- Key points: Industry adoption, breakthrough applications, future potential
- Visual: Icons showing different ML applications

... (continue for all slides)
```

### Step 2: Generate Each Slide

Use `generate_slide_image.py` to create each slide.

**CRITICAL: Formatting Consistency Protocol**

To ensure unified formatting across all slides:

1. **Define a Formatting Goal** at the start and include it in EVERY prompt:
   - Color scheme (e.g., "dark blue background, white text, gold accents")
   - Typography style (e.g., "bold sans-serif titles, clean body text")
   - Visual style (e.g., "minimal, professional, corporate aesthetic")
   - Layout approach (e.g., "generous white space, left-aligned content")

2. **Always attach the previous slide** when generating subsequent slides using `--attach`:
   - This allows Nano Banana Pro to see and match the existing style
   - Creates visual continuity throughout the deck
   - Ensures consistent colors, fonts, and design language

3. **Default author is "K-Dense"** unless another name is specified

4. **Include citations directly in the prompt** for slides that reference research:
   - Add citations in the prompt text so they appear on the generated slide
   - Use format: "Include citation: (Author et al., Year)" or "Show reference: Author et al., Year"
   - For multiple citations, list them all in the prompt
   - Citations should appear in small text at the bottom of the slide or near relevant content

5. **Attach existing figures/data for results slides** (CRITICAL for data-driven presentations):
   - When creating slides about results, ALWAYS check for existing figures
   - Use `--attach` to include these figures so Nano Banana Pro can incorporate them
   - When attaching data figures, describe what you want in the prompt
   - Multiple figures can be attached: `--attach fig1.png --attach fig2.png`

### Step 3: Combine to PDF

```bash
# Combine all slides into a PDF presentation
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

## Example Workflow

```bash
# Title slide (first slide - establishes the style)
python scripts/generate_slide_image.py "Title slide for presentation: 'Machine Learning: From Theory to Practice'. Subtitle: 'AI Conference 2025'. Speaker: K-Dense. FORMATTING GOAL: Dark blue background (#1a237e), white text, gold accents (#ffc107), minimal design, sans-serif fonts, generous margins, no decorative elements." -o slides/01_title.png

# Content slide with citations (attach previous slide for consistency)
python scripts/generate_slide_image.py "Presentation slide titled 'Why Machine Learning Matters'. Three key points with simple icons: 1) Industry adoption, 2) Breakthrough applications, 3) Future potential. CITATIONS: Include at bottom in small text: (LeCun et al., 2015; Goodfellow et al., 2016). FORMATTING GOAL: Match attached slide style - dark blue background, white text, gold accents, minimal professional design, no visual clutter." -o slides/02_intro.png --attach slides/01_title.png

# RESULTS SLIDE - Attach actual data figure from working directory
python scripts/generate_slide_image.py "Presentation slide titled 'Model Performance Results'. Create a slide presenting the attached accuracy chart. Key findings to highlight: 1) 95% accuracy achieved, 2) Outperforms baseline by 12%, 3) Consistent across test sets. CITATIONS: Include at bottom: (Our results, 2025). FORMATTING GOAL: Match attached slide style exactly." -o slides/04_results.png --attach slides/03_background.png --attach figures/accuracy_chart.png

# Combine to PDF
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

## Prompt Template

Include these elements in every prompt (customize as needed):
```
[Slide content description]
CITATIONS: Include at bottom: (Author1 et al., Year; Author2 et al., Year)
FORMATTING GOAL: [Background color], [text color], [accent color], minimal professional design, no decorative elements, consistent with attached slide style.
```

## Script Options

### generate_slide_image.py

```bash
# Full slide (default) - generates complete slide as image
python scripts/generate_slide_image.py "slide description" -o output.png

# Visual only - generates just the image/figure for embedding in PPT
python scripts/generate_slide_image.py "visual description" -o output.png --visual-only

# With reference images attached
python scripts/generate_slide_image.py "Create a slide explaining this chart" -o slide.png --attach chart.png
python scripts/generate_slide_image.py "Combine these into a comparison slide" -o compare.png --attach before.png --attach after.png
```

**Options:**
- `-o, --output`: Output file path (required)
- `--attach IMAGE`: Attach image file(s) as context for generation (can use multiple times)
- `--visual-only`: Generate just the visual/figure, not a complete slide
- `--iterations`: Max refinement iterations (default: 2)
- `--api-key`: OpenRouter API key (or set OPENROUTER_API_KEY env var)
- `-v, --verbose`: Verbose output

### slides_to_pdf.py

```bash
# Combine PNG files
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf

# Combine specific files in order
python scripts/slides_to_pdf.py title.png intro.png methods.png -o talk.pdf

# From directory (sorted by filename)
python scripts/slides_to_pdf.py slides/ -o presentation.pdf
```

**Options:**
- `-o, --output`: Output PDF path (required)
- `--dpi`: PDF resolution (default: 150)
- `-v, --verbose`: Verbose output

**Tip:** Name slides with numbers for correct ordering: `01_title.png`, `02_intro.png`, etc.

## Environment Setup

```bash
export OPENROUTER_API_KEY='your_api_key_here'
# Get key at: https://openrouter.ai/keys
```

## Quick Start Example

For a 15-minute conference talk:

1. **Plan** (30 minutes):
   - Use research-lookup to find 8-12 relevant papers
   - Build outline (intro → methods → 2-3 key results → conclusion)
   - Create detailed plan for each slide
   - Target 15-18 slides

2. **Generate** (1-2 hours):
   - Use consistent formatting across all slides
   - Attach previous slide each time
   - Include citations where relevant

3. **Review & Iterate** (30 minutes):
   - Open PDF and review each slide
   - Regenerate slides that need improvement

4. **Practice** (2-3 hours):
   - Practice 3-5 times with timer
   - Aim for 13-14 minutes (leave buffer)

Total time: ~4-5 hours for quality presentation
