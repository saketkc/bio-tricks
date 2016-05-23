#!/bin/bash
## Make mm9 Phylop30Way bigwig
set -euo pipefail
rsync -avz --progress rsync://hgdownload.cse.ucsc.edu/goldenPath/mm9/phyloP30way/vertebrate/* ./
gunzip *.gz
mkdir random
mv *_random.wigFix random
cat *.wigFix > mm9.30way.phyloP.wig
wigToBigWig mm9.30way.phyloP.wig ../fasta/mm9.chrom.sizes mm9.30way.phyloP.bw
