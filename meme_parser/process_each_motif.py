#!/usr/bin/env python

from Bio import motifs
import glob
import sys
import os
import subprocess

__base_location__ = '/media/data1/ENCODE/'
__phyloP100way__ = '/media/data1/HSapiens/hg19/hg19.100way.phyloP100way.wig'
__phyloP46way__ = '/media/data1/HSapiens/hg19/hg19.100way.phyloP46way.wig'
__genome_table__ = '/home/saket/genomes/hg19.chrom.sizes'

def get_motifs(meme_file):
    handle = open(meme_file, 'r')
    records = motifs.parse(handle, 'meme')
    total_motifs = len(records)
    return total_motifs

def main(argv):
    tech_repl = '1'
    bio_repl = '1'
    arg = argv[0]
    path = os.path.join(__base_location__, argv[0], 'tech_repl_{}'.format(tech_repl), 'bio_repl_{}'.format(bio_repl),'analysis', 'quest_output_withIP','conservation_analysis')
    os.chdir(path)
    meme_file = os.path.join(path, 'meme_analysis', 'meme.txt')
    flanking_sequences = []
    for f in glob.glob("*.flanking_sequences.fa"):
        flanking_sequences.append(os.path.join(path,f))
    if len(flanking_sequences)>1:
        sys.stderr.write('[Error] More than 1 flanking_sequences present for '.format(arg))
        sys.exit(1)
    total_motifs = get_motifs(os.path.join(path, 'meme_analysis', 'meme.txt'))
    for motif in range(1, total_motifs+1):
        fimo_path = os.path.join(path, 'fimo_analysis_with_flanking_motif_{}'.format(motif))
        subprocess.call(['fimo', '--motif', str(motif),
                            '-oc',  fimo_path,
                            meme_file,
                            '{}'.format(flanking_sequences[0])], cwd=path)
        fimo_in = os.path.join(fimo_path, 'fimo.txt')
        fimo_2_out = os.path.join(fimo_path, 'fimo_2_sites.txt')
        phyloP100way_out = os.path.join(fimo_path, '100way_site_conservation.txt')
        phyloP46way_out = os.path.join(fimo_path, '46way_site_conservation.txt')
        subprocess.call(['fimo_2_sites', 'fimo_file={}'.format(fimo_in), 'output_file={}'.format(fimo_2_out)], cwd=path)
        subprocess.call(['calculate_site_conservation',
                            'sites_file={}'.format(fimo_2_out),
                            'genome_table={}'.format(__genome_table__),
                            'wig_file={}'.format(__phyloP100way__),
                            'output_file={}'.format(phyloP100way_out)], cwd=path)
        subprocess.call(['calculate_site_conservation',
                            'sites_file={}'.format(fimo_2_out),
                            'genome_table={}'.format(__genome_table__),
                            'wig_file={}'.format(__phyloP46way__),
                            'output_file={}'.format(phyloP46way_out)], cwd=path)
        subprocess.call(['meme_processor.py',
                            '-i', meme_file,
                            '-c', '{}.{}'.format(phyloP100way_out,'stats'),
                            '-m', str(motif)], cwd=fimo_path)
        subprocess.call(['meme_processor.py',
                            '-i', meme_file,
                            '-c', '{}.{}'.format(phyloP46way_out,'stats'),
                            '-m', str(motif)], cwd=fimo_path)

if __name__ == '__main__':
    main(sys.argv[1:])
