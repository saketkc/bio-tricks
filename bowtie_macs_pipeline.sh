#!/usr/bin/bash
bowtie -p 4 -M 1 -q -v 2 -k 1 -X 2000 --best --strata --sam /usr/local/share/bcbio/genomes/Hsapiens/hg19/bowtie/hg19 -1 $1 -2 $2 "$3.sam"
samtools view -@ 4 -h -S -b "$3.sam" -o "$3.bam"
samtools sort "$3.bam"  "$3.sorted"
sambamba index -t 4 "$3.sorted.bam" "$3.sorted.bam.bai"
bedtools bamtobed -i "$3.sorted.bam" > "$3.sorted.bed"
macs2 callpeak -t "$3.sorted.bed" --nomodel --nolambda --extsize 75 --SPMR -g hs -n "$3.macs2"
