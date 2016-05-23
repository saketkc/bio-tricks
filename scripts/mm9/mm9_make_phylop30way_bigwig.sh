#!/bin/bash
set -euo pipefail
rsync -avz --progress rsync://hgdownload.cse.ucsc.edu/goldenPath/mm9/phyloP30way/vertebrate/* ./
gunzip -f *.gz
mkdir -p random
mv *_random.* random
cat *.wigFix > mm9.30way.phyloP.wig
wigToBigWig mm9.30way.phyloP.wig ../fasta/mm9.chrom.sizes mm9.30way.phyloP.bw
