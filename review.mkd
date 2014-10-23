---
title: "Review: Transposition of native chromatin for fast and sensitive epigenomic profiling of open chromatin, DNA-binding proteins and nucleosome position Jason"
author: "Saket Choudhary"

---

##Summary
###Aim: 

Study the interplay between open chromatin regions, DNA binding proteins and 
individual nucleosomes.

### Who Cares:
A new in vitro technique for studying how DNA binding factors interact with nucelosome bound/free regions which further aids studying gene regulation

###Need

Problems with DNAse techniques:

- Large cell sample size, leading to an 'averaging' out of the heterogenity
- Need for large sample size forces culture growth incubated ex vivo thus diluting the in vivo context
- Large processing times, limited clinical applicability!


###How
Hypothesis: Transposase Tn5(found in prokaryotes) when mixed with the eukaryoitc cells integrates the adaptors only at regions that are part of the accessible chromatin.
Transposition(shifting of the gene location) is difficult in regions that are bound to nucelosome.
The 'peaks' will therefore come from regions that are in open chromatin are nucelosome free.

###Datasets
Cells isolated from GM12878 human lymphoblastoid cell line. 

###Reason for the choice of datasets
GM12878 is a lymphoblastoid cell line produced from the blood of a female donor with northern and western European ancestry by EBV transformation.[Ref](http://www.genome.gov/26524238)

The focus was on the locus that has been shown in a [previous study](http://www.nature.com/nature/journal/v489/n7414/full/nature11232.html) to achieve the high signal/noise ratio with the validation being done through DNAase and FAIRE seq experiments

NOTE :  The peaks from the figure seem to be occuring at RBM42 ETV2 ZBTB32 MLL4 IGFLR1 HSPB6 ARHGAP33

## Validation Criteria

- Similar peaks in DNAase seq
- Same peaks in technical replicates
- > ATAC-seq peak intensities also correlated well with markers of active chromatin and not
   with transposase sequence preference
   
## Inferences

- ATAC Seq captured nucleosome sites
    - The insert size distribution of the reads showed the original fragments appearing in preiodicity of ~150 which is a good number since core DNA[DNA bound about nucleosomes] should be 147 bp while the linker DNA is 20-60bp.  Now if you somehow managed to capture two nucelosomes you should see 150+150+60 = 360 and with three that would be 150+60+150+60+150=500
    
## Nucleosome positioning
 Partition data into reads generate from possibly the nucleosome rich region.
 


