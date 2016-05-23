#!/bin/bash
## Make mm9 PhastCons60Way bigwig
set -euo pipefail
rsync -avz --progress rsync://hgdownload.cse.ucsc.edu/goldenPath/mm9/phastCons60way/vertebrate/ ./
gunzip -f *.gz
mkdir -p random
mv *_random.data random
cat *.data > mm9.60way.phastCons.wig
wigToBigWig mm9.60way.phastCons.wig ../fasta/mm9.chrom.sizes mm9.60way.phastCons.bw
