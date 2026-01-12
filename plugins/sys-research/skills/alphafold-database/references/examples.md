# AlphaFold Database Examples

## Example 1: Basic Protein Structure Retrieval

```python
from alphafold.database import AlphaFoldDB

# Initialize client
db = AlphaFoldDB()

# Retrieve structure for a protein
uniprot_id = "P00533"  # EGFR human protein
structure = db.retrieve_structure(unipot_id)

print(f"Retrieved structure: {structure.uniprot_id}")
print(f"Confidence (pLDDT): {structure.confidence:.2f}")
```

## Example 2: Bulk Download with Progress Tracking

```python
import asyncio
from alphafold.database import AlphaFoldDB

async def download_multiple_proteins(uniprot_ids):
    """Download multiple protein structures asynchronously."""
    db = AlphaFoldDB()

    async for structure in db.bulk_retrieve(uniprot_ids):
        structure.save_to_file(f"{structure.uniprot_id}.pdb")
        print(f"Downloaded: {structure.uniprot_id}")

# Download a list of proteins
proteins = ["P00533", "Q00981", "P04637"]
asyncio.run(download_multiple_proteins(proteins))
```

## Example 3: Confidence Analysis

```python
from alphafold.database import AlphaFoldDB
from alphafold.analysis import analyze_confidence

# Retrieve structure
db = AlphaFoldDB()
structure = db.retrieve_structure("P00533")

# Analyze confidence
analysis = analyze_confidence(structure.confidence)

print(f"Average confidence: {analysis.avg_confidence:.2f}")
print(f"High confidence regions: {analysis.high_confidence_percentage:.1f}%")
print(f"Low confidence regions: {analysis.low_confidence_percentage:.1f}%")

# Get confidence by residue
for residue_id, confidence in structure.get_confidence_per_residue():
    if confidence < 50:
        print(f"Residue {residue_id}: Low confidence ({confidence:.1f})")
```

## Example 4: PAE Analysis

```python
from alphafold.database import AlphaFoldDB

# Retrieve structure
db = AlphaFoldDB()
structure = db.retrieve_structure("P00533")

# Analyze predicted aligned error
pae_matrix = structure.pae

# Find domain boundaries
domains = structure.find_domain_boundaries(pae_threshold=10)

print(f"Predicted domains: {domains}")
for i, domain in enumerate(domains):
    print(f"Domain {i+1}: residues {domain.start} - {domain.end}")
```

## Example 5: Integration with PyMOL

```python
from alphafold.database import AlphaFoldDB
from pymol import cmd

# Retrieve structure
db = AlphaFoldDB()
structure = db.retrieve_structure("P00533")

# Load into PyMOL
cmd.load(structure.pdb_file, "protein")
cmd.color("red", "byexp")  # Color by experimental confidence

# Highlight low confidence regions
cmd.select("low_confidence", f"b < 50")
cmd.color("yellow", "low_confidence")

cmd.save("protein_highlighted.pse")
print("Structure saved to protein_highlighted.pse")
```

## Example 6: Custom Analysis Pipeline

```python
from alphafold.database import AlphaFoldDB
from alphafold.analysis import (
    analyze_confidence,
    analyze_domains,
    calculate_surface_area
)

def analyze_protein(uniprot_id):
    """Complete protein analysis pipeline."""
    db = AlphaFoldDB()

    # Retrieve structure
    structure = db.retrieve_structure(uniprot_id)

    # Perform analyses
    confidence_analysis = analyze_confidence(structure.confidence)
    domain_analysis = analyze_domains(structure.pae)
    surface_analysis = calculate_surface_area(structure.coordinates)

    # Generate report
    report = {
        "uniprot_id": uniprot_id,
        "confidence": {
            "average": confidence_analysis.avg_confidence,
            "high_confidence_residues": confidence_analysis.high_confidence_percentage,
            "low_confidence_residues": confidence_analysis.low_confidence_percentage
        },
        "domains": {
            "count": len(domain_analysis.domains),
            "boundaries": domain_analysis.domains
        },
        "surface_area": surface_analysis.total_area,
        "structure_quality": "good" if confidence_analysis.avg_confidence > 80 else "moderate"
    }

    return report

# Run analysis
report = analyze_protein("P00533")
print(f"Analysis complete: {report}")
```

## Example 7: Batch Processing with Filtering

```python
from alphafold.database import AlphaFoldDB
from alphafold.filters import ConfidenceFilter, SizeFilter

# Define filters
filters = [
    ConfidenceFilter(min_avg_confidence=70),
    SizeFilter(min_residues=100, max_residues=1000)
]

# Process with filters
db = AlphaFoldDB()
structures = db.filter_and_retrieve(uniprot_ids, filters)

for structure in structures:
    print(f"High-quality structure: {structure.uniprot_id} "
          f"(confidence: {structure.confidence:.1f}, "
          f"residues: {structure.num_residues})")
```

## Example 8: Structural Comparison

```python
from alphafold.database import AlphaFoldDB
from alphafold.comparison import compare_structures

# Retrieve two structures
db = AlphaFoldDB()
structure1 = db.retrieve_structure("P00533")
structure2 = db.retrieve_structure("Q00981")

# Compare structures
comparison = compare_structures(structure1, structure2)

print(f"RMSD: {comparison.rmsd:.2f} Å")
print(f"Similarity score: {comparison.similarity:.2f}")
print(f"Aligned residues: {comparison.aligned_residues}")

# Save aligned structure
comparison.save_aligned_structure("aligned.pdb")
```

## Example 9: Integration with MDAnalysis

```python
import MDAnalysis as mda
from alphafold.database import AlphaFoldDB

# Retrieve structure
db = AlphaFoldDB()
structure = db.retrieve_structure("P00533")

# Load into MDAnalysis
u = mda.Universe(structure.pdb_file)

# Calculate radius of gyration
rg = u.atoms.radius_of_gyration()
print(f"Radius of gyration: {rg:.2f} Å")

# Find secondary structure
for segment in u.atoms.segments:
    print(f"Segment {segment.segid}: {len(segment.atoms)} atoms")

# Export to other formats
u.atoms.write("protein.dcd")  # Trajectory format
```

## Example 10: Automated Report Generation

```python
import json
from alphafold.database import AlphaFoldDB
from alphafold.analysis import analyze_confidence

def generate_protein_report(uniprot_id, output_file):
    """Generate comprehensive protein analysis report."""
    db = AlphaFoldDB()
    structure = db.retrieve_structure(uniprot_id)

    # Perform analyses
    confidence = analyze_confidence(structure.confidence)

    # Generate report
    report = {
        "protein_id": uniprot_id,
        "sequence_length": structure.num_residues,
        "analysis_date": datetime.now().isoformat(),
        "confidence_metrics": {
            "average_plddt": round(confidence.avg_confidence, 2),
            "high_confidence_percentage": round(confidence.high_confidence_percentage, 2),
            "low_confidence_percentage": round(confidence.low_confidence_percentage, 2),
            "regions": [
                {
                    "start": region.start,
                    "end": region.end,
                    "confidence": region.avg_confidence,
                    "quality": region.quality_label
                }
                for region in confidence.regions
            ]
        },
        "files": {
db": structure.pdb_file,
            "mmcif": structure            "p.mmcif_file,
            "confidence_json": structure.confidence_json,
            "pae_json": structure.pae_json
        }
    }

    # Save report
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"Report saved to {output_file}")
    return report

# Generate report
report = generate_protein_report("P00533", "protein_analysis.json")
```

## Best Practices

1. **Always check confidence scores** before analysis
2. **Use bulk downloads** for multiple proteins
3. **Filter by quality** for reliable results
4. **Cache downloaded structures** to avoid re-downloading
5. **Validate UniProt IDs** before retrieval
6. **Handle errors gracefully** with try-except blocks
7. **Use async downloads** for better performance
8. **Save intermediate results** for debugging
9. **Document analysis parameters** for reproducibility
10. **Validate against experimental structures** when available

## Error Handling

```python
from alphafold.exceptions import (
    ProteinNotFoundError,
    DownloadError,
    InvalidConfidenceError
)

try:
    structure = db.retrieve_structure("INVALID_ID")
except ProteinNotFoundError as e:
    print(f"Protein not found: {e}")
except DownloadError as e:
    print(f"Download failed: {e}")
except InvalidConfidenceError as e:
    print(f"Invalid confidence data: {e}")
```
