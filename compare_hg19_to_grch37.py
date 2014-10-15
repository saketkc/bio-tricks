#!/usr/bin/env python
"""
This script compares the difference between hg19 and GRCh37.
GRCh37 is supposedly the NCBI equivalent of UCSC's hg19.
See: http://seqanswers.com/forums/archive/index.php/t-9757.html

However the posts on the forum are not really convincing. There are more insights here:
    http://uswest.ensembl.org/Help/Faq?id=286

    Point #1: Ensembl uses a one-based coordinate system, whereas UCSC uses a zero-based coordinate system.
    Ensembl:  ATCG
              1234
    UCSC:     ATCG
              0123

    For display UCSC browser uses 1-based coordinate system.[http://genome.ucsc.edu/FAQ/FAQtracks.html#tracks1]
    Point #2: Ensembl uses the most recently updated human genome housed at the GRC.
    This current major assembly release is called GRCh38. NCBI and UCSC use the same genome.
    UCSC refers to the recent human genome as GRCh38/hg38. Before all that let's see what these coordinate sytems
    are all about. Blatantly copying from the SAM1 specification[http://samtools.github.io/hts-specs/SAMv1.pdf]:

    1-based coordinate system: A coordinate system where the first base of a sequence is one. In this
    coordinate system, a region is specified by a closed interval. For example, the region between
    the 3rd and the 7th bases inclusive is [3, 7]. The SAM, VCF, GFF and Wiggle formats are using
    the 1-based coordinate system.

    0-based coordinate system: A coordinate system where the first base of a sequence is zero. In this
    coordinate system, a region is specified by a half-closed-half-open interval. For example, the
    region between the 3rd and the 7th bases inclusive is [2, 7). The BAM, BCFv2, BED, and PSL
    formats are using the 0-based coordinate system.]


    chrX  	|  A  |  T  |  G  |  C  |  A  |  T  |  C  |  G  |
    0-based	0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8
    1-based        1	 2     3     4     5     6     7     8

    So expanding from the SAM1 specifications:
    1. Ranged nucleotides will be represented as:
        i) 0-based chrX:2-7 GCATC
       ii) 1-based chrX:3-7 GCATC
    2. From point 1. a single nucleotide is represented as:
        i) 0-based chrX:7-8 G
       ii) 1-based chrX:8-8 G
    3. SNPs will be:
        i) 0-based chrX:7-8 G/A
       ii) 1-based chrX:8-8 G/A

   Insertions and deletions are tricky:
                                                                    X
    chrX        |  A  |  T  |  G  |  C  |  A  |  T  |  C  |  C  |  ATC  G  |
    0-based     0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8       |  9
    1-based        1     2     3     4     5     6     7     8          9


    ATC is inserted in between C & G of the original sequence.
    1. INSertions:
        i) 0-based chrX:8-8 -/ATC
       ii) 1-based chrX:8-9 -/ATC

    2. DELetion:
        i) 0-based chrX:4-5 A/-
       ii) 1-based chrX:5-5 A/-

    Example[https://code.google.com/p/bedtools/wiki/FAQ#What_does_zero-based,_half-open_mean?]: $ cat first_base.bed
    chr1    0       1       i-am-the-first-position-on-chrom1

    Given the examples the conversion is straighforward:
    For nucleotides, SNP, DEL:
            (1-based start) = (0-based start + 1)
            (1-based end)   = (0-based end)
    For insertion:
            (1-based start) = (0-based start)
            (1-based end)   = (0-based end + 1)

    Why a 0-based system?
    It makes the calculations simple:
    Consider chrX0-2 ATC & chrX1-4 ATCG
    ATC
     ATCG
    Length of overlap = min(end1, end2) - max(start1, start2) = 2-0 = 2
    Whereas for a 1-based system:
    chrX1-3 ATC & chrX2-5 ATCG
    ATC
     ATCG
    Length of overlap = min(end1, end2) - max(start1, start2) = 3-2 = 1 => WRONG! Why? You need to add 1
    It is intituitive if you think of the numbers between(including) 1 & 5 is  5-1+1=5! [1,2,3,4,5]

    An important note for uploading data to UCSC Genome browser:
        If you submit data to the browser in position format (chr#:##-##),
        the browser assumes this information is 1-based.
        If you submit data in any other format (BED (chr# ## ##) or otherwise),
        the browser will assume it is 0-based.
        You can see this both in our liftOver utility and in our search bar,
        by entering the same numbers in position or BED format and observing the results.
        Similarly, any data returned by the browser in position format is 1-based, while data returned in BED format is 0-based.


    Coming back to hg19 and GRCh37 stuff:
        The GRCh37 assembly defintion is at: ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/All/GCF_000001405.13.assembly.txt
        Besides Chromos 1-22, there are these things called 'unlocalized-scaffold' and 'unplaced-scaffold'.
        Let's head over to the definitions of the Consortium: http://www.ncbi.nlm.nih.gov/projects/genome/assembly/grc/info/definitions.shtml

        unlocalized-scaffold:
            A sequence found in an assembly that is associated with a specific chromosome but cannot be ordered or oriented on that chromosome.
            e.g HSCHR17_RANDOM_CTG2 associated with chromosome 17, but cannot be oriented on it

        unplaced-scaffold:
            A sequence found in an assembly that is not associated with any chromosome.
            e.g. HSCHRUN_RANDOM_CTG2

        Cool. Here is the hg19 equivalent[http://genome.ucsc.edu/FAQ/FAQdownloads.html#download12]:
        http://hgdownload.cse.ucsc.edu/goldenpath/hg19/chromosomes/

            chrN_random_[table]:
                In the past, these tables contained data related to sequence that is known to be in a particular chromosome, but could not be reliably ordered within the current sequence.
                E.g. chr21_gl000210_random.fa.gz
            ChrUn:
                ChrUn contains clone contigs that can't be confidently placed on a specific chromosome.
                E.g  chrUn_gl000237
        Another note:
            UCSC's hg19 has chrM as the mitochondiral DNA.
            Note on chrM:
                Since the release of the UCSC hg19 assembly, the Homo sapiens mitochondrion
                sequence (represented as "chrM" in the Genome Browser) has been replaced in
                GenBank with the record NC_012920. We have not replaced the original sequence,
                NC_001807, in the hg19 Genome Browser. We plan to use the Revised Cambridge
                Reference Sequence (rCRS, http://mitomap.org/bin/view.pl/MITOMAP/HumanMitoSeq)
                in the next human assembly release




"""
from Bio import SeqIO
import pickle
from pprint import pprint
import sys
hg19_location = "/usr/local/share/bcbio/genomes/Hsapiens/hg19/hg19.fa"
grch37_location = "/usr/local/share/bcbio/genomes/Hsapiens/GRCh37/bowtie/GRCh37.fa"
try:
    pickled = pickle.load(open('comparison_pickled.p', 'rb'))
    print (pickled)
    sys.exit(0)
except Exception as e:
    print e
hg19_handle = open(hg19_location, 'rU')
hg19_chromosomes = {}
for record in SeqIO.parse(hg19_handle,  'fasta'):
    hg19_chromosomes[record.id] = len(record)
hg19_handle.close()


grch37_handle = open(grch37_location, 'rU')
grch37_chromosomes = {}
for record in SeqIO.parse(grch37_handle, 'fasta'):
    grch37_chromosomes[record.id] = len(record)
grch37_handle.close()


pickle_string = "GRCh37\n"
for key, value in grch37_chromosomes.iteritems():
    pickle_string +=  key + ":"  + str(value) + "\n"

pickle_string += "\nhg19\n"
for key, value in hg19_chromosomes.iteritems():
    pickle_string +=  key + ":" + str(value) + "\n"


for i in range(1,23):
    pickle_string += str(i) + " => " + "GRCh37: " + str(grch37_chromosomes[str(i)]) + " || hg19: " + str(hg19_chromosomes['chr' + str(i)]) + "\n"
    assert(grch37_chromosomes[str(i)] == hg19_chromosomes['chr' + str(i)])
pickle.dump(pickle_string, open('comparison_pickled.p', 'wb'))
