#!/bin/bash
mkdir -p phylop && cd phylop
wget -c http://hgdownload-test.cse.ucsc.edu/goldenPath/ce9/bigZips/ce9.chrom.sizes
wget -c http://hgdownload-test.cse.ucsc.edu/goldenPath/ce9/phyloP10way/phyloP10way.wigFix.gz
gunzip phyloP10way.wigFix.gz
wigToBigWig phyloP10way.wigFix ce9.chrom.sizes ce9.phyloP10way.bw

