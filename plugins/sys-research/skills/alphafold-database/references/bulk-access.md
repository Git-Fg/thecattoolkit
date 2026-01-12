# Bulk Data Access

## Access Methods

### Google Cloud Platform
- **Full proteome downloads**
- **Location:** `gs://alphafold-databases/`
- **Format:** Multiple file formats
- **Access:** gsutil command-line tool

### FTP Server
- **Bulk downloads via FTP**
- **URL:** `ftp.ebi.ac.uk/pub/databases/alphafold/`
- **Structure:** Organized by organism
- **Access:** Standard FTP clients

### API Access
- **Programmatic retrieval**
- **Endpoints:** REST API
- **Features:** Query, filter, metadata
- **Rate limits:** Check documentation

## Bulk Download Strategies

### Organism-Level Downloads
```
# Download complete proteome for organism
organism/
├── taxonomy_id.txt
├── uniprot/
├── pdb/
└── mmcif/
```

### Selective Downloads
- By taxonomic group
- By protein family
- By confidence threshold
- By file format

## Programmatic Bulk Access

### Python Example
```python
import os
from Bio.PDB import alphafold_db

# Download multiple proteins
uniprot_ids = ["P00520", "P04637", "P01133"]

for uniprot_id in uniprot_ids:
    try:
        predictions = list(alphafold_db.get_predictions(uniprot_id))
        for prediction in predictions:
            cif_file = alphafold_db.download_cif_for(
                prediction,
                directory="./bulk_structures"
            )
            print(f"Downloaded {uniprot_id}: {cif_file}")
    except Exception as e:
        print(f"Error downloading {uniprot_id}: {e}")
```

### Using gsutil
```bash
# List available datasets
gsutil ls gs://alphafold-databases/

# Download full proteome
gsutil -m cp -r gs://alphafold-databases/uniprot_v4/ ./uniprot_v4/

# Download specific organism
gsutil -m cp -r gs://alphafold-databases/uniprot_v4/9606/ ./human_proteome/
```
