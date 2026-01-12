# PowerPoint Workflow Guide

Create editable PowerPoint presentations by generating visuals with Nano Banana Pro, then building PPTX slides with text.

## Why PowerPoint Workflow?

**Advantages**:
- Editable slides (can modify text later)
- Complex animations and transitions
- Interactive elements
- Company template compatibility

**Best for**: Editable presentations, custom designs, template-based workflows, corporate environments

## Overview

When creating PowerPoint presentations, use Nano Banana Pro to generate images and figures for each slide, then add text separately using the PPTX skill.

**How it works:**
1. **Plan the deck**: Create content plan for each slide
2. **Generate visuals**: Use Nano Banana Pro with `--visual-only` flag to create images for slides
3. **Build PPTX**: Use the PPTX skill (html2pptx or template-based) to create slides with generated visuals and separate text

## Step-by-Step Process

### Step 1: Generate Visuals for Each Slide

Use `generate_slide_image.py` with the `--visual-only` flag to create images for embedding in slides.

```bash
# Generate a figure for the introduction slide
python scripts/generate_slide_image.py "Professional illustration showing machine learning applications: healthcare diagnosis, financial analysis, autonomous vehicles, and robotics. Modern flat design, colorful icons on white background." -o figures/ml_applications.png --visual-only

# Generate a diagram for the methods slide
python scripts/generate_slide_image.py "Neural network architecture diagram showing input layer, three hidden layers, and output layer. Clean, technical style with node connections. Blue and gray color scheme." -o figures/neural_network.png --visual-only

# Generate a conceptual graphic for results
python scripts/generate_slide_image.py "Before and after comparison showing improvement: left side shows cluttered data, right side shows organized insights. Arrow connecting them. Professional business style." -o figures/results_visual.png --visual-only
```

### Step 2: Build PowerPoint with PPTX Skill

Use the PPTX skill's html2pptx workflow to create slides that include:
- Generated images from step 1
- Title and body text added separately
- Professional layout and formatting

**Reference**: See `document-skills/pptx/SKILL.md` for complete PPTX creation documentation.

## Key Resources

### Design Guide
- `assets/powerpoint_design_guide.md`: Complete PowerPoint design guide

### PPTX Skill Scripts
From `document-skills/pptx/scripts/`:
- `thumbnail.py`: Create thumbnail grids for visual validation
- `rearrange.py`: Duplicate and reorder slides
- `inventory.py`: Extract text content
- `replace.py`: Update text programmatically

### Workflow Methods

**Option A: Programmatic (html2pptx)**
1. Design HTML slides with generated visuals
2. Use html2pptx to convert to PowerPoint
3. Add text and formatting programmatically

**Option B: Template-Based**
1. Choose or create PowerPoint template
2. Insert generated visuals into slides
3. Add text content
4. Customize layout and formatting

## Visual Generation Tips

For images to embed in PowerPoint, focus on the visual element only:

```
"Flowchart showing machine learning pipeline: Data Collection → Preprocessing → Model Training → Validation → Deployment. Clean technical style, blue and gray colors."

"Conceptual illustration of cloud computing with servers, data flow, and connected devices. Modern flat design, suitable for business presentation."

"Scientific diagram of cell division process showing mitosis phases. Educational style with labels, colorblind-friendly colors."
```

## Design Considerations

### Color Palettes
Choose modern color palettes reflecting your topic:
- **Biotech**: Vibrant colors (teal, coral, emerald)
- **Physics**: Sleek darks (navy, charcoal, silver)
- **Health**: Warm tones (warm blues, greens, soft reds)
- **Tech**: Bold contrasts (electric blue, white, gray)

NOT just default blue/gray themes.

### Typography
- Sans-serif fonts (Arial, Calibri, Helvetica)
- Large fonts: 24-28pt for body text
- 36-44pt for slide titles
- High contrast (minimum 4.5:1, prefer 7:1)

### Layout
- Vary layouts (not all bullet lists)
- Use two-column layouts (text + figure)
- Full-slide figures for key results
- Asymmetric compositions
- Rule of thirds for focal points
- Consistent but not repetitive

## Integration with Other Skills

### Research Lookup
Use for:
- Background development
- Citation gathering
- Gap identification
- Prior work comparison
- Supporting evidence
- Question preparation

### Data Visualization
Use for:
- Creating presentation-appropriate figures
- Simplifying complex visualizations
- Ensuring readability from distance
- Using progressive disclosure

## Validation Workflow

### Generate Thumbnails
```bash
# Using the pdf_to_images script
python scripts/pdf_to_images.py presentation.pdf review/slide --dpi 150

# Or use pptx skill's thumbnail tool
python ../document-skills/pptx/scripts/thumbnail.py presentation.pptx review/thumb
```

### Systematic Review
1. View each slide image
2. Check against quality checklist:
   - Text overflow
   - Element overlap
   - Font sizes (≥18pt)
   - Contrast (≥4.5:1)
   - Layout issues
   - Visual quality
3. Document problems with slide numbers
4. Fix identified issues in source
5. Regenerate and re-inspect

## Quick Start Example

1. **Plan** slides with content and visual requirements
2. **Generate visuals** with `--visual-only` flag:
   ```bash
   python scripts/generate_slide_image.py "diagram description" -o figures/fig1.png --visual-only
   ```
3. **Build PPTX** using the PPTX skill with generated images
4. **Add text** separately using PPTX workflow
5. **Validate** with thumbnail generation
6. **Iterate** based on visual inspection

See `document-skills/pptx/SKILL.md` for complete PowerPoint workflow documentation.
