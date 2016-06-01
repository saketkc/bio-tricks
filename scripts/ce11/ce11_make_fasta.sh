
#!/bin/bash
set -eo pipefail
mkdir -p fasta && cd phyloP
wget -c http://hgdownload-test.cse.ucsc.edu/goldenPath/ce11/bigZips/ce11.2bit
twoBitToFa ce11.2bit ce11.fa
wget -c http://hgdownload-test.cse.ucsc.edu/goldenPath/ce11/bigZips/ce11.chrom.sizes
