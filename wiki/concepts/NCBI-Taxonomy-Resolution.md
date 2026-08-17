---
title: "NCBI Taxonomy Resolution"
type: concept
tags:
  - bioinformatics/taxonomy
  - ncbi/entrez
  - classification/organism
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - Taxonomy Resolution
  - Lineage Mapping
  - TaxID Extraction
---

# NCBI Taxonomy Resolution

**NCBI Taxonomy Resolution** is the process of mapping sequence accessions and BLAST alignment hit titles to formal biological taxa, TaxIDs (Taxonomy Identifiers), and complete phylogenetic lineages.

---

## 1. The Challenge in BLAST Output

BLAST hit definition lines (e.g. from `blastn` or `blastp`) frequently present formatting challenges:
- GI tags and accession strings embedded in the title (e.g. `gi|887494115|gb|KT232088.1|`).
- Incomplete or ambiguous descriptions (e.g., `Synthetic construct clone pXYZ`, `Uncultured bacterium clone`).
- Missing species brackets in legacy records.

---

## 2. Extraction & Fallback Architecture

In the Mystery Sequence Identifier pipeline ([`sequence_io.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py)):

```mermaid
graph TD
    A[BLAST Hit Title] --> B{Regex Match Bracket [Organism]?}
    B -- Yes --> C[Extract Scientific Name]
    B -- No --> D{Known Keyword Boundaries?}
    D -- Yes --> E[Slice Before 'complete cds', 'gene', etc.]
    D -- No --> F[Mark as 'Unknown Organism']
    F --> G[Trigger Entrez Metadata Fallback]
    G --> H[Query Entrez efetch / esummary]
    H --> I[Parse Organism & Lineage]
```

### Fallback Tiers:
1. **Header Parsing**: Fast, local extraction using regex heuristics on hit definition lines (`extract_organism_from_title`).
2. **Entrez `efetch` (GenBank XML/Text)**: Queries NCBI E-Utilities (`rettype="gb"`) to retrieve official `/organism` and `/db_xref="taxon:XXXX"` annotations.
3. **Entrez `esummary`**: Retrieves document summaries for title and taxonomy metadata when full flat files are unavailable.

---

## 3. Phylogenetic Lineage Traversal

Once an organism is resolved to a TaxID, its complete taxonomic hierarchy can be traversed:

$$\text{Superkingdom} \rightarrow \text{Phylum} \rightarrow \text{Class} \rightarrow \text{Order} \rightarrow \text{Family} \rightarrow \text{Genus} \rightarrow \text{Species} \rightarrow \text{Strain / Isolate}$$

This hierarchical information enables:
- Resolving ambiguous multi-hit alignments to the lowest common ancestor (LCA).
- Distinguishing natural organism origins from laboratory cloning vectors or recombinant expression constructs.

---

## Cross-References
- [[NCBI-Entrez]]
- [[module-sequence-io]]
- [[BLAST-Alignment-Filtering]]
- [[Pipeline-Architecture]]
