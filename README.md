# LampreyExonCapture

## About
This code is for the data assembly steps of the following paper:
> Hughes, L.C., Bloom, D.B., Piller, K.R., Lang, N., Mayden, R.L. Phylogenomic Resolution of Lampreys Reveals the Recent Evolution of an Ancient Vertebrate Lineage. Accepted. Proceedings of the Royal Society B: Biological Sciences.


The general pipeline based on ray-finned fish reference sequences is described in:
> Hughes, L.C., Ortí, G., Saad, H., Chenhog, L., White, W.T., Baldwin, C.C., Crandall, K.A., Arcila, D., and Betancur-R., R. 2021. Exon probe sets and bioinformatics pipelines for all levels of fish phylogenomics. *Molecular Ecology Resources*, 21(3):816-833. DOI:10.1111/1755-0998.13287

## Dependencies
- Python3
- [aTRAM2](https://github.com/juliema/aTRAM)
- BLAST+
- Trinity
- exonerate
- cd-hit

## Files
1. PetromyzonFishLife.fa
> Reference sequences for targeted based on the *Petromyzon marinus* genome for aTRAM.
2. Run-aTRAM.py
> After quality trimming raw reads with Trimmomatic, this script runs the aTRAM pipeline using Trinity as the assembler.
3. Post-aTRAM-Filtering.py
> Runs cd-hit to get the longest assembled sequences, and exonerate to find ORFs. These filtering steps are described in detail in Hughes _et al._ (2021).
