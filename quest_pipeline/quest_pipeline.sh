#!/bin/bash
set -ex
################Paths#####################
export jobName="H1-hESC_CTCF_ENCSR000AMF/H1-hESC_Control_ENCSR000AMI"
export encodeID="ENCFF000AVG"
export tech_repl="1"
export bio_repl="1"
export path="/media/data1/ENCODE/$jobName/tech_repl_$tech_repl/"
export bamF="$path/bio_repl_$bio_repl/$encodeID.bam"
export outDir="/media/data1/ENCODE/$jobName/tech_repl_$tech_repl/bio_repl_$bio_repl/analysis"
mkdir -p $outDir
export samF="$outDir/$encodeID.sam"
################Paths#####################


cd $outDir
bamtosam.sh $bamF "$samF"
generate_QuEST_parameters.pl -sam_align_ChIP "$samF" -rp ~/genomes/chromosomes/ -gt ~/genome/hg19.chrom.sizes -ap quest_output
cat ./quest_output/calls/peak_caller.ChIP.out.accepted | grep "R-" | awk '{print $2"\t"$9"\t"$5}' > $encodeID.peaks
sort -k3nr  $encodeID.peaks > $encodeID.sorted.peaks
extract_sequence_chuncks_near_sites output=$encodeID.sequence_chunks.fasta
meme
fimo
fimo_2_sites
calculate_site_conservation

