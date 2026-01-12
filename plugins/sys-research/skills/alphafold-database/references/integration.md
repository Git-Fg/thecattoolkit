# Integration with Analysis Tools

## PyMOL Integration

### Loading and Visualizing Structures
```python
# Load structure in PyMOL
cmd.load("model_v4.cif", "protein")
cmd.show("cartoon", "protein")
cmd.color("confidence", "protein")

# Color by pLDDT confidence
cmd.load("confidence_v4.json", "confidence")
cmd.ramp_new("confidence_bar", "confidence", [0, 50, 100])
cmd.set_color("high_conf", [0, 1, 0])  # Green
cmd.set_color("med_conf", [1, 1, 0])    # Yellow
cmd.set_color("low_conf", [1, 0, 0])   # Red
```

### Custom Visualization Scripts
```python
# Color by confidence level
cmd.select("high_conf", f"protein and confidence > 70")
cmd.select("med_conf", f"protein and confidence between 50 and 70")
cmd.select("low_conf", f"protein and confidence < 50")

cmd.color("green", "high_conf")
cmd.color("yellow", "med_conf")
cmd.color("red", "low_conf")
```

## MDAnalysis Integration

### Loading and Analyzing Structures
```python
import MDAnalysis as mda

# Load mmCIF structure
u = mda.Universe("model_v4.cif")
protein = u.select_atoms("protein")

# Analyze structure
radius_gyration = protein.radius_of_gyration()
print(f"Radius of gyration: {radius_gyration:.2f} Å")

# Calculate secondary structure
from MDAnalysis.analysis import secondary_structure
ss = secondary_structure.SecondaryStructure(u, sel="protein")
ss.run()
```

### Time Series Analysis
```python
# For multi-model structures
for ts in u.trajectory:
    rg = protein.radius_of_gyration()
    print(f"Frame {ts.frame}: Rg = {rg:.2f}")
```

## Biopython Integration

### Structure Analysis
```python
from Bio.PDB import MMCIFParser, PDBIO

# Parse structure
parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "model_v4.cif")

# Analyze residues
for model in structure:
    for chain in model:
        print(f"Chain {chain.id}: {len(chain)} residues")

# Calculate B-factors (use pLDDT as B-factor)
for atom in structure.get_atoms():
    # Use pLDDT score as B-factor for visualization
    atom.set_bfactor(confidence_score)
```

## Plotting and Visualization

### Matplotlib Integration
```python
import matplotlib.pyplot as plt
import json

# Plot pLDDT confidence
with open("confidence_v4.json") as f:
    confidence = json.load(f)

plt.figure(figsize=(12, 6))
plt.plot(confidence['plddt'])
plt.xlabel('Residue Position')
plt.ylabel('pLDDT Score')
plt.title('AlphaFold Confidence Profile')
plt.axhline(y=70, color='g', linestyle='--', label='High Confidence')
plt.axhline(y=50, color='y', linestyle='--', label='Medium Confidence')
plt.legend()
plt.show()
```

### Seaborn for Advanced Plots
```python
import seaborn as sns
import numpy as np

# Plot PAE heatmap
with open("predicted_aligned_error_v4.json") as f:
    pae = json.load(f)['pae']

plt.figure(figsize=(10, 10))
sns.heatmap(pae, cmap='viridis', cbar_kws={'label': 'PAE'})
plt.title('Predicted Aligned Error (PAE) Matrix')
plt.show()
```

## Computational Pipelines

### Automated Workflow
```python
def analyze_protein(uniprot_id):
    """Complete analysis workflow for a protein"""
    # 1. Download structure
    predictions = list(alphafold_db.get_predictions(uniprot_id))
    cif_file = alphafold_db.download_cif_for(predictions[0])

    # 2. Load confidence data
    with open("confidence_v4.json") as f:
        confidence = json.load(f)

    # 3. Calculate statistics
    mean_plddt = np.mean(confidence['plddt'])
    high_conf_residues = sum(1 for x in confidence['plddt'] if x > 70)

    return {
        'uniprot_id': uniprot_id,
        'mean_plddt': mean_plddt,
        'high_confidence_percent': high_conf_residues / len(confidence['plddt']) * 100,
        'structure_file': cif_file
    }
```

### Batch Processing
```python
# Process multiple proteins
uniprot_list = ["P00520", "P04637", "P01133"]
results = []

for uniprot_id in uniprot_list:
    try:
        result = analyze_protein(uniprot_id)
        results.append(result)
    except Exception as e:
        print(f"Error processing {uniprot_id}: {e}")

# Save results
import pandas as pd
df = pd.DataFrame(results)
df.to_csv("alphafold_analysis.csv", index=False)
```
