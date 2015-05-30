#!/usr/bin/env python
"""
Process meme.txt files to
generate conservation plots
"""
import argparse
import sys

from Bio import motifs

def plot_meme_against_phylo(meme_record, phylo):
    pass

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
    #parser.add_argument('-c', '--phylo', metavar='<phylo_out>', help='PhyloP conservation scores', required=True)
    parsed = parser.parse_args(argv)
    handle = open(parsed.meme)
    records = motifs.parse(handle, 'meme')
    record = records[parsed.motif]
    #with open(parsed.phylo,'r') as f:
        #phylo = f.read()
    profile = position_wise_profile(record.pwm, record.length)
    max_occur = find_max_occurence(profile)
    print max_occur[0]

if __name__ == "__main__":
    main(sys.argv[1:])
