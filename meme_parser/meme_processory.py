#!/usr/bin/env python
"""
Process meme.txt files to
generate conservation plots
"""
import argparse
import csv
import sys
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from Bio import motifs

def plot_meme_against_phylo(meme_record, phylo):
    sns.set(style="darkgrid")


def position_wise_profile(counts_dict, length):
    profile = map(dict, zip(*[[(k, v) for v in value] for k, value in counts_dict.items()]))
    return profile

def find_max_occurence(profile, max_count=2):
    sorted_profile = []
    for p in profile:
        sorted_profile.append(sorted(p.items(), key=lambda x:x[1]))
    for i,p in enumerate(sorted_profile):
        sorted_profile[i] = p[-max_count:]
    return sorted_profile


def main(argv):
    parser = argparse.ArgumentParser(description='Process meme files')
    parser.add_argument('-i', '--meme', metavar='<meme_out>', help='Meme input file', required=True)
    parser.add_argument('-m', '--motif', metavar='<motif_no>', help='Motif number', required=True, type=int)
    parser.add_argument('-c', '--phylo', metavar='<phylo_out>', help='PhyloP conservation scores', required=True)
    parsed = parser.parse_args(argv)
    handle = open(parsed.meme)
    records = motifs.parse(handle, 'meme')
    record = records[parsed.motif-1]
    phylo_data = csv.reader(open(parsed.phylo,'r'), delimiter='\t')
    phylo_scores = []
    for line in phylo_data:
        phylo_scores.append(float(line[2]))
    print "Motif length", record.length
    print "phylo length", len(phylo_scores)
    profile = position_wise_profile(record.counts, record.length)
    max_occur = find_max_occurence(profile, max_count=1)
    motif_scores = []
    for position in max_occur:
        motif_scores.append(position[0][1])
    pr = pearsonr(np.array(motif_scores), np.array(phylo_scores))
    fig, ax = plt.subplots()
    ax= sns.regplot(y=np.array(motif_scores), x=np.array(phylo_scores), scatter=True)
    ax.set(ylabel="Motif Counts", xlabel="PhyloP scores", title='CTCF | pearsonr = {}'.format(pr[0]));
    fig.savefig('scatter.png')
    x = np.linspace(1,len(phylo_scores)+1,num=len(phylo_scores), endpoint=False)
    print x
    f, (ax1, ax2) = plt.subplots(2, 1)
    x1 = sns.barplot(x,y=np.array(motif_scores), ax=ax1)
    x2 = sns.barplot(x,y=np.array(phylo_scores), ax=ax2)
    x1.set(ylabel='Motif counts', xlabel='Position in motif')
    x2.set(ylabel='Phylop Score', xlabel='Position in motif')
    f.tight_layout()
    f.savefig('tight.png')
if __name__ == "__main__":
    main(sys.argv[1:])
