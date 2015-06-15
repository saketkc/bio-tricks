[Source](https://groups.google.com/forum/#%21topic/meme-suite/rIbjIHbcpAE)
1) Limit the size of the input file. 
When there are 1000s of peaks, MEME can find the main motif easily in just a *subsample* of the peaks. There is not much to be gained by including more than 1000 peaks, and MEME run time will increase greatly. 

As of MEME release 4.4.0 patch 1 the MEME distribution contains a perl script called "fasta-subsample". This perl script lets you select the number of sequences you want in your new file. Keep the number of sequences under 1000 for reasonable MEME run times. Also, if the total length of sequences is 100,000 expect run times of about 20 minutes per motif (DNA, -revcomp, ZOOPS). 

A typical use would be: 
fasta-subsample all_chip_seqs.fasta 500 -rest cv.fasta -seed 1 > meme.fasta

2) Keep the input sequences short. 
MEME works best if you keep the size of the sequences (centered on the ChIP-seq peak) to 300bp or less. In our experience, the vast majority of the actual binding sites are in this region, and longer sequences makes it much harder to detect weak motifs and co-factor motifs. 

The -off and -len switches to "fasta-subsample" can be used to trim the peak sequences in order to keep them less than 300bp long. 

3) Use the ZOOPS model and both strands 
The ZOOPS model with the -revcomp switch is usually the best choice for running MEME on ChIP-seq data. The following command has worked well for us with ChIP-seq peak sequences: 
meme meme.fasta -dna -revcomp -minw 5 -maxw 20


4) Cross-validate your results 
To get a cross-validated estimate of the fraction of your ChIP-seq sequences that show significant binding, you can use the AMA (average motif affinity) program. Run "ama" on the set of "left-out" sequences (ones not given in input to MEME) using a command like: 
ama --pvalues meme_out/meme.html cv.fasta bfile > cv.ama


The file "bfile", which contains the base frequencies for all your ChIP-seq peaks, should be made using the command: 
fasta-get-markov < all_chip_seqs.fasta > bfile


To get the q-values and "pi_0", the fraction of sequences not showing significant binding in the held out set, run the script "ama-qvalues" (also in release 4.4.0 patch 1) on your AMA score file: 
ama-qvalues < cv.ama


The value of "pi_0" is printed at the bottom of the output. Note--If there are fewer than 100 sequences in "cv.ama", no estimate of pi_0 is printed. The output also shows the p-value and q-value of the AMA score for each sequence in the file of "held-out" sequences. (Q-value is the minimum False Discovery Rate at which a score would be considered significant. 

5) Repeat the cross-validation to verify the results 
To get a better idea of the stability of the results, repeat from step 1), above, but using a different value for the "-seed" in the "fasta-subsample" command. This will cause a different random split of the ChIP-seq sequence set. Ideally, the motif discovered by MEME in step 3) each time will be similar, as will the estimates of the number of binding sequences in step 4).

