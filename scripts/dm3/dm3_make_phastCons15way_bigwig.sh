#!/bin/bash
## Make dm3 PhastCons15Way bigwig
set -euo pipefail
rsync -avz --progress rsync://hgdownload.cse.ucsc.edu/goldenPath/dm3/phastCons15way/ ./
for f in *.gz
do
    gunzip -c "$f" > "${f%.gz}"
done
## Select one value for chr2R since there is an overlap
## Otherwise causes this:
## There's more than one value for chr2R base 5000001 (in coordinates that start with 1).

sed -i.orig -e '4963003d' chr2R.pp

## Fix for:
## There's more than one value for chr3L base 7000001 (in coordinates that start with 1).

sed -i.orig -e '6969685d' chr3R.pp


## Fix for:
## There's more than one value for chrX base 12000001 (in coordinates that start with 1).

sed -i.orig -e '11943831d' chrX.pp

## Fix for:
## There's more than one value for chr3L base 7000001 (in coordinates that start with 1).
## There's more than one value for chr3L base 11000001 (in coordinates that start with 1).
## There's more than one value for chr3L base 19000001 (in coordinates that start with 1).


sed -i.orig -e '6993258d;10989627d;18983630d' chr3L.pp

cat *.pp > dm3.15way.phastCons.wig
wigToBigWig dm3.15way.phastCons.wig ../fasta/dm3.chrom.sizes dm3.15way.phastCons.bw
