#!/bin/bash
## Make ce6 PhastCons6Way bigwig
set -euo pipefail
rsync -avz --progress rsync://hgdownload.cse.ucsc.edu/goldenPath/ce6/phastCons6way/ ./
gunzip -f *.gz
cat *.data > ce6.6way.phastCons.wig
wigToBigWig ce6.6way.phastCons.wig ../fasta/ce6.chrom.sizes ce6.6way.phastCons.bw
