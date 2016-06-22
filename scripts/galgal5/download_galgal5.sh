#!/bin/bash
wget -r -c -nH --cut-dirs=100 ftp://ftp.ncbi.nih.gov/genomes/Gallus_gallus/Assembled_chromosomes/seq/
wget -r -c -nH --cut-dirs=100 ftp://ftp.ncbi.nih.gov/genomes/refseq/vertebrate_other/Gallus_gallus/latest_assembly_versions/GCF_000002315.4_Gallus_gallus-5.0/GCF_000002315.4_Gallus_gallus-5.0_genomic.fna.gz
