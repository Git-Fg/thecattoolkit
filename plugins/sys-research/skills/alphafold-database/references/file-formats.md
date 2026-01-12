# File Formats

## Available File Types

AlphaFold provides multiple file formats for each prediction:

- **Model coordinates** (`model_v4.cif`): Atomic coordinates in mmCIF/PDBx format
- **Confidence scores** (`confidence_v4.json`): Per-residue pLDDT scores (0-100)
- **Predicted Aligned Error** (`predicted_aligned_error_v4.json`): PAE matrix for residue pair confidence
- **Additional features** (`features.json`): MSA, domain boundaries, etc.

## mmCIF/PDBx Format

- **Use:** Structural analysis, visualization
- **Tools:** PyMOL, ChimeraX, MDAnalysis
- **Content:** Atomic coordinates, residues, chains
- **Extension:** `.cif`

## JSON Format

- **Use:** Programmatic analysis
- **Tools:** Python, R, JavaScript
- **Content:** Confidence metrics, features, metadata
- **Files:**
  - `confidence_v4.json` - pLDDT scores
  - `predicted_aligned_error_v4.json` - PAE matrix
  - `features.json` - Additional features

## File Naming Convention

```
AF-[UniProtID]-[version].cif                    # mmCIF coordinates
AF-[UniProtID]-[version]_confidence.json        # pLDDT scores
AF-[UniProtID]-[version]_predicted_aligned_error.json  # PAE matrix
AF-[UniProtID]-[version]_features.json          # Features
```

Example: `AF-P00520-F1-model_v4.cif`
