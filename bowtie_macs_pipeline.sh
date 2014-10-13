#!/usr/bin/bash
bowtie -p 4 -M 1 -q -v 2 -k 1 -X 2000 --best --strata --sam GRCh37.fa -1 SRR891275_1.fastq -2 SRR891275_2.fastq GSM1155964_bowtie.sam
samtools sort  GSM1155964_bowtie.bam GSM1155964_bowtie.sorted
sambamba index -t 4 GSM1155964_bowtie.sorted.bam GSM1155964_bowtie.sorted.bam.bai
bedtools bamtobed GSM1155964_bowtie.sorted.bam > GSM1155964_bowtie-ready.bed
macs2 callpeak -t GSM1155964_bowtie-ready.bed --nomodel --nolambda --extsize 75 --SPMR -g hs -n rep1
