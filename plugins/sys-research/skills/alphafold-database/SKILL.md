---
name: alphafold-database
description: "Retrieves structures by UniProt ID, downloads PDB/mmCIF files, and analyzes confidence metrics (pLDDT, PAE) for drug discovery and structural biology research. Use when accessing AlphaFold's 200M+ AI-predicted protein structures."
allowed-tools: [Read, Write, Edit, Bash]
---

# AlphaFold Database

## Overview

AlphaFold DB is a public repository of AI-predicted 3D protein structures for over 200 million proteins, maintained by DeepMind and EMBL-EBI. Access structure predictions with confidence metrics, download coordinate files, retrieve bulk datasets, and integrate predictions into computational workflows.

## When to Use This Skill

Use when working with AI-predicted protein structures for:
- Retrieving predictions by UniProt ID or protein name
- Downloading PDB/mmCIF coordinate files for analysis
- Analyzing confidence metrics (pLDDT, PAE) for reliability assessment
- Accessing bulk proteome datasets via cloud platforms
- Comparing with experimental data
- Performing structure-based drug discovery or protein engineering
- Building structural models for proteins lacking experimental structures
- Integrating predictions into computational pipelines

## Core Capabilities

### 1. Structure Retrieval
```python
from Bio.PDB import alphafold_db
predictions = list(alphafold_db.get_predictions("P00520"))
cif_file = alphafold_db.download_cif_for(predictions[0], directory="./structures")
```

### 2. File Formats
- **mmCIF/PDBx** (`model_v4.cif`): Atomic coordinates
- **JSON** (`confidence_v4.json`): pLDDT confidence scores
- **JSON** (`predicted_aligned_error_v4.json`): PAE matrix
- **JSON** (`features.json`): MSA, domain boundaries

### 3. Confidence Metrics
- **pLDDT** (0-100): Per-residue confidence
- **PAE**: Predicted Aligned Error matrix
- **pTM**: Overall template modeling score

### 4. Bulk Access
- Google Cloud Platform downloads
- FTP server access
- Programmatic API retrieval

**See:** `references/retrieval-methods.md` for complete retrieval guide

## Quick Examples

### Basic Retrieval
```python
from Bio.PDB import alphafold_db
predictions = list(alphafold_db.get_predictions("P00520"))
cif_file = alphafold_db.download_cif_for(predictions[0])
```

### Analyze Confidence
```python
import json, matplotlib.pyplot as plt

with open("confidence_v4.json") as f:
    confidence = json.load(f)

plt.plot(confidence['plddt'])
plt.title('pLDDT Confidence Scores')
plt.show()
```

**See:** `references/examples.md` for complete worked examples

## File Formats

### mmCIF/PDBx
- **Use:** Structural analysis, visualization
- **Tools:** PyMOL, ChimeraX, MDAnalysis

### JSON
- **Use:** Programmatic analysis
- **Content:** Confidence metrics, features, metadata

**See:** `references/file-formats.md` for detailed format documentation

## Confidence Interpretation

### pLDDT Scores
- **90-100:** Very high confidence
- **70-90:** High confidence
- **50-70:** Medium confidence
- **0-50:** Low confidence

### PAE Matrix
- N×N matrix where N = protein length
- Lower values indicate higher confidence
- Useful for domain boundary prediction

**See:** `references/confidence-analysis.md` for detailed analysis methods

## Common Use Cases

### Drug Discovery
1. Retrieve target structure
2. Analyze binding site confidence
3. Identify high-confidence regions
4. Compare with experimental data

### Protein Engineering
1. Analyze PAE for domain boundaries
2. Identify flexible regions
3. Design mutations in high-confidence areas
4. Validate predictions

### Structural Comparison
1. Retrieve AlphaFold prediction
2. Download experimental structure
3. Align and calculate RMSD
4. Analyze differences

**See:** `references/use-cases.md` for detailed workflows

## Best Practices

### Recommended Practices
- Check pLDDT scores (>70 for reliable regions)
- Validate with experimental data when available
- Use appropriate file formats for your analysis
- Cite AlphaFold database and version

### Avoid
- Relying on low-confidence regions (pLDDT < 50)
- Ignoring experimental context
- Using outdated database versions

**See:** `references/best-practices.md` for complete guidelines

## Integration

### PyMOL
```python
cmd.load("model_v4.cif", "protein")
cmd.show("cartoon", "protein")
```

### MDAnalysis
```python
import MDAnalysis as mda
u = mda.Universe("model_v4.cif")
protein = u.select_atoms("protein")
```

**See:** `references/integration.md` for complete integration examples

## Reference Materials

**Core Implementation:**
- `references/retrieval-methods.md` - All retrieval methods and examples
- `references/file-formats.md` - Complete format documentation
- `references/confidence-analysis.md` - Confidence metric analysis
- `references/bulk-access.md` - Bulk data access methods

**Use Cases & Workflows:**
- `references/use-cases.md` - Common use cases
- `references/best-practices.md` - Best practices and guidelines
- `references/integration.md` - Integration with analysis tools

**Quick Start:**
1. Install Biopython: `pip install biopython`
2. Retrieve structure by UniProt ID
3. Download coordinate files
4. Analyze confidence metrics
5. Integrate into your workflow
