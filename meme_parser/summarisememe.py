#!/usr/bin/env python

from Bio import motifs
import sys


def main(argv):
    handle = open(argv[0], 'r')
    records = motifs.parse(handle, 'meme')
    print "Total motifs present: {}".format(len(records))
    for i, record in enumerate(records):
        print "Motif {} \t Length: {} \t, Seq: {}".format(i, len(record.consensus), record.consensus)
if __name__ == '__main__':
    main(sys.argv[1:])
