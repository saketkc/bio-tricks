#!/bin/bash
## Make dm3 PhastCons15Way bigwig
set -euo pipefail
rsync -avz --progress rsync://hgdownload.cse.ucsc.edu/goldenPath/dm3/phastCons15way/ ./
gunzip -f *.gz
cat *.pp > dm3.15way.phastCons.wig
wigToBigWig dm3.15way.phastCons.wig ../fasta/dm3.chrom.sizes dm3.15way.phastCons.bw
