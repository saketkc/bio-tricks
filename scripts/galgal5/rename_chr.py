'''
Rename chromosomes downloaded from Genbank to sane chromosome ids
'''

from __future__ import print_function
import re
import sys
from Bio import SeqIO

def rename(source, target):
    '''Rename chrs in source to target'''
    chr_regex = re.compile(r'chromosome (\d|\w)+|chrUn_.*,|chr\d.*,|chrW.*,|chrZ.*,|chrLGE.*,|mitochondrion|group LGE64')
    with open(source, 'r') as fs, open(target, 'w') as fo:
        records = SeqIO.parse(fs, 'fasta')
        for record in records:
            desc = record.description
            chrid = chr_regex.search(desc).group(0)
            new_chrid = chrid.replace('chromosome ', 'chr')\
                    .replace(',', '')\
                    .replace('mitochondrion', 'chrM')\
                    .replace('group LGE64', 'LGE64')
            record.description = new_chrid
            record.id = new_chrid
            SeqIO.write(record, fo, 'fasta')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Run: python rename_chr.py <source.fasta> <target.fasta>')
        sys.exit(1)
    rename(sys.argv[1], sys.argv[2])
