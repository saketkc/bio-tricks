#!/usr/bin/env python
'''
Encode data downloader(BAM/FastQ)
'''
import os
import json
import sys
import subprocess
import requests

ROOT_DIR = '/media/data1/ENCODE'
FILE_TYPE = 'bam' #'fastq'

BASE_URL = 'https://www.encodeproject.org/'
def parser(encode_id):
    req = requests.get('https://www.encodeproject.org/experiments/{}/?format=json'.format(encode_id))
    response_json = req.json()
    biosample = response_json['biosample_term_name']
    label = response_json['target']['label']
    files = response_json['files']
    replicates = len(response_json['replicates'])
    controls = response_json['possible_controls']
    metadata = {}
    for f in files:
        href = f['href']
        if f['file_type'] == FILE_TYPE:
            if replicates == 1:
                bio_repl = 1
                tech_repl = 1
            else:
                try:
                    bio_repl = f['replicate']['biological_replicate_number']
                    tech_repl = f['replicate']['technical_replicate_number']
                except KeyError:
                    bio_repl = f['biological_replicates'][0]
                    tech_repl = 1

            if tech_repl not in metadata.keys():
                metadata[tech_repl] = {}
            if bio_repl not in metadata[tech_repl].keys():
                metadata[tech_repl][bio_repl] = {}
            metadata[tech_repl][bio_repl] = {'href': href, 'metadata':f}
    return {'replicates': replicates, 'controls': controls, 'label': label, 'files': files, 'biosample':biosample, 'metadata':metadata}

def downloader(files, metadata, path):
    for tech_repl in metadata.keys():
        for bio_repl in metadata[tech_repl].keys():
            href = BASE_URL + metadata[tech_repl][bio_repl]['href']
            mdata = metadata[tech_repl][bio_repl]['metadata']
            location = os.path.join(path, 'tech_repl_{}'.format(tech_repl), 'bio_repl_{}'.format(bio_repl))
            try:
                os.makedirs(location)
            except OSError:
                pass
            with open(os.path.join(location, 'metadata.json'), 'w') as w:
                json.dump(mdata, w)
            subprocess.call(['wget', '-c', href, '-P', location])


def control_downloader(controls=[], TF_data_path=''):
    print len(controls)
    for control in controls:
        encode_id = control['accession']
        print 'Downloading control: ', encode_id
        parsed = parser(encode_id)
        biosample = parsed['biosample']
        label = parsed['label']
        metadata = parsed['metadata']
        files = parsed['files']
        job_name = '{}_{}_{}'.format(biosample, label, encode_id)
        downloader(files, metadata, os.path.join(TF_data_path, job_name))



def encode_downloader(args):
    for encode_id in args:
        encode_id = args[0]
        parsed = parser(encode_id)
        biosample = parsed['biosample']
        label = parsed['label']
        controls = parsed['controls']
        replicates = parsed['replicates']
        files = parsed['files']
        job_name = '{}_{}_{}'.format(biosample, label, encode_id)
        metadata = parsed['metadata']
        path = os.path.join(ROOT_DIR, job_name)
        print 'Downloading controls'#, controls
        control_downloader(controls, path)
        downloader(files, metadata, path)

if __name__=='__main__':
    if len(sys.argv)<2:
        print 'Run: $ python encode_downloader.py <encode_id1> <encode_id2> ...'
        sys.exit(1)
    encode_downloader(sys.argv[1:])
