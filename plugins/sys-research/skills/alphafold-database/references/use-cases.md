# Common Use Cases

## Use Case 1: Structure-Based Drug Discovery

### Workflow
1. Retrieve target protein structure
2. Analyze confidence scores for binding sites
3. Identify high-confidence regions for docking
4. Compare with experimental structures

### Key Steps
```python
# 1. Download structure
from Bio.PDB import alphafold_db
predictions = list(alphafold_db.get_predictions("P00520"))
cif_file = alphafold_db.download_cif_for(predictions[0])

# 2. Load and analyze confidence
with open("confidence_v4.json") as f:
    confidence = json.load(f)

# 3. Identify high-confidence regions (>70 pLDDT)
high_confidence = [i for i, score in enumerate(confidence['plddt']) if score > 70]

# 4. Focus docking on these regions
```

### Best Practices
- Focus on pLDDT > 80 regions
- Validate binding sites experimentally
- Check PAE for domain boundaries

## Use Case 2: Protein Engineering

### Workflow
1. Download protein of interest
2. Analyze PAE for domain boundaries
3. Identify flexible regions
4. Design mutations in high-confidence areas

### Key Steps
```python
# 1. Load PAE matrix
with open("predicted_aligned_error_v4.json") as f:
    pae_data = json.load(f)

# 2. Analyze for domain boundaries
# Look for block-diagonal structure in PAE
plt.imshow(pae_data['pae'], cmap='viridis')
plt.show()

# 3. Identify flexible regions (high PAE values)
flexible_regions = [i for i in range(len(pae_data['pae']))
                    if max(pae_data['pae'][i]) > 20]
```

### Best Practices
- Design mutations in pLDDT > 70 regions
- Avoid flexible regions for critical residues
- Consider PAE for domain boundary prediction

## Use Case 3: Structural Comparison

### Workflow
1. Retrieve AlphaFold prediction
2. Download experimental structure
3. Align structures using RMSD
4. Analyze differences in low-confidence regions

### Key Steps
```python
# 1. Load AlphaFold structure
af_structure = MMCIFParser().get_structure("AF", "AF-P00520-F1-model_v4.cif")

# 2. Load experimental structure
exp_structure = MMCIOarser().get_structure("EXP", "experimental.pdb")

# 3. Align structures
superimposer = Superimposer()
superimposer.set_atoms(af_structure, exp_structure)
superimposer.apply(af_structure)

# 4. Calculate RMSD
rmsd = superimposer.rms
```

### Best Practices
- Use high-confidence regions for alignment
- Compare multiple experimental structures
- Focus analysis on structural differences
