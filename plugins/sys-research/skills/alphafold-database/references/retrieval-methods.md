# Retrieval Methods

## Using Biopython (Recommended)

```python
from Bio.PDB import alphafold_db

# Get all predictions for a UniProt accession
predictions = list(alphafold_db.get_predictions("P00520"))

# Download structure file (mmCIF format)
for prediction in predictions:
    cif_file = alphafold_db.download_cif_for(prediction, directory="./structures")
    print(f"Downloaded: {cif_file}")

# Get Structure objects directly
from Bio.PDB import MMCIFParser
structures = list(alphafold_db.get_structural_models_for("P00520"))
```

## Quick Retrieval Examples

### Example 1: Retrieve and Download
```python
from Bio.PDB import alphafold_db

# Get predictions for a protein
predictions = list(alphafold_db.get_predictions("P00520"))

# Download the best prediction
best_prediction = predictions[0]
cif_file = alphafold_db.download_cif_for(best_prediction, directory="./structures")
```

### Example 2: Analyze Confidence
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
plt.show()
```

## Alternative Methods

### Direct File Downloads
- Access AlphaFold FTP server
- Download specific UniProt entries
- Programmatic batch downloads

### API Access
- REST API for programmatic retrieval
- Bulk dataset access
- Metadata queries
