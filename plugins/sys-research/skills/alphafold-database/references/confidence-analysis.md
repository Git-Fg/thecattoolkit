# Confidence Metrics Analysis

## Key Metrics

### pLDDT (Per-Residue Confidence)
- **Range:** 0-100
- **Interpretation:**
  - 90-100: Very high confidence
  - 70-90: High confidence
  - 50-70: Medium confidence
  - 0-50: Low confidence

### PAE (Predicted Aligned Error)
- **Matrix:** N×N where N = protein length
- **Values:** 0-30+ (lower is better)
- **Use:** Domain boundary prediction, model quality assessment

### pTM (Template Modeling Score)
- **Range:** 0-1
- **Use:** Overall model quality assessment
- **Threshold:** > 0.8 indicates good overall fold

## Analyzing Confidence

### Load and Visualize pLDDT Scores
```python
import json
import matplotlib.pyplot as plt

# Load confidence scores
with open("confidence_v4.json") as f:
    confidence_data = json.load(f)

# Plot pLDDT scores
plddt_scores = confidence_data['plddt']
plt.plot(plddt_scores)
plt.title('pLDDT Confidence Scores')
plt.xlabel('Residue Position')
plt.ylabel('pLDDT Score')
plt.show()
```

### Analyze PAE Matrix
```python
import numpy as np
import matplotlib.pyplot as plt

# Load PAE data
with open("predicted_aligned_error_v4.json") as f:
    pae_data = json.load(f)

# Visualize PAE matrix
plt.imshow(pae_data['pae'], cmap='viridis')
plt.colorbar(label='Predicted Aligned Error')
plt.title('PAE Matrix')
plt.show()

# Identify domain boundaries
# Look for low-error diagonal blocks
```

## Confidence Interpretation Guidelines

### High-Confidence Regions (pLDDT > 70)
- Reliable for structural analysis
- Suitable for docking studies
- Good for binding site identification

### Medium-Confidence Regions (pLDDT 50-70)
- Use with caution
- Validate with experimental data
- May indicate flexible regions

### Low-Confidence Regions (pLDDT < 50)
- Avoid for critical analysis
- Likely intrinsically disordered
- Consider experimental validation
