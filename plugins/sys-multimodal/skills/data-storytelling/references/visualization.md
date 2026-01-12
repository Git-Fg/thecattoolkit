# Visualization Techniques

## Technique 1: Progressive Reveal

```markdown
Start simple, add layers:

Slide 1: "Revenue is growing" [single line chart]
Slide 2: "But growth is slowing" [add growth rate overlay]
Slide 3: "Driven by one segment" [add segment breakdown]
Slide 4: "Which is saturating" [add market share]
Slide 5: "We need new segments" [add opportunity zones]
```

## Technique 2: Contrast and Compare

```markdown
Before/After:
┌─────────────────┬─────────────────┐
│    BEFORE       │     AFTER       │
│                 │                 │
│  Process: 5 days│  Process: 1 day │
│  Errors: 15%   │  Errors: 2%     │
│  Cost: $50/unit │  Cost: $20/unit │
└─────────────────┴─────────────────┘

This/That (emphasize difference):
┌─────────────────────────────────────┐
│         CUSTOMER A vs B             │
│  ┌──────────┐    ┌──────────┐      │
│  │ ████████ │    │ ██       │      │
│  │ $45,000  │    │ $8,000   │      │
│  │ LTV      │    │ LTV      │      │
│  └──────────┘    └──────────┘      │
│  Onboarded       No onboarding     │
└─────────────────────────────────────┘
```

## Technique 3: Annotation and Highlight

```python
import matplotlib.pyplot as plt
import pandas as pd

fig, ax = plt.subplots(figsize=(12, 6))

# Plot the main data
ax.plot(dates, revenue, linewidth=2, color='#2E86AB')

# Add annotation for key events
ax.annotate(
    'Product Launch\n+32% spike',
    xy=(launch_date, launch_revenue),
    xytext=(launch_date, launch_revenue * 1.2),
    fontsize=10,
    arrowprops=dict(arrowstyle='->', color='#E63946'),
    color='#E63946'
)

# Highlight a region
ax.axvspan(growth_start, growth_end, alpha=0.2, color='green',
           label='Growth Period')

# Add threshold line
ax.axhline(y=target, color='gray', linestyle='--',
           label=f'Target: ${target:,.0f}')

ax.set_title('Revenue Growth Story', fontsize=14, fontweight='bold')
ax.legend()
```

## Visualization Principles

### Choose the Right Chart Type

**For Comparisons:**
- Bar charts for categorical data
- Stacked bars for composition
- Grouped bars for multi-category comparison

**For Trends:**
- Line charts for time series
- Area charts for cumulative trends
- Slope charts for before/after

**For Relationships:**
- Scatter plots for correlations
- Bubble charts for 3D data
- Heatmaps for matrix data

### Color Strategy

**High Contrast:**
- Primary: #2E86AB (blue)
- Secondary: #A23B72 (purple)
- Accent: #F18F01 (orange)
- Alert: #E63946 (red)
- Success: #06A77D (green)

**Usage:**
- Use accent colors sparingly for emphasis
- Gray for non-important elements
- Red for warnings, green for success

### Typography

**Font Hierarchy:**
- Headline: 18-24pt, bold
- Subhead: 14-16pt, semi-bold
- Body: 10-12pt, regular
- Caption: 8-10pt, italic

**Spacing:**
- Leave whitespace around data
- Use gridlines sparingly
- Avoid overcrowding labels
