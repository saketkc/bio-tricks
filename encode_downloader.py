#!/usr/bin/env python
import requests
#import argparse
import subprocess
import sys
import os

__base_url__ = 'https://www.encodeproject.org/'
download_prefix = "/media/data1/ENCODE"

def encode_downloader(args):
    encode_id = args[0]
    req = requests.get("https://www.encodeproject.org/experiments/{}/?format=json".format(encode_id))
    json = req.json()
    files = json['files']
    ## Metadata format: {technical_replicate_number: {biological_replicate_number1: url, biological_replicate_number2: url}}
    metadata = {}
    for f in files:
        href = f['href']
        if f['file_type']== 'bam':
            bio_repl = f['replicate']['biological_replicate_number']
            tech_repl = f['replicate']['technical_replicate_number']
            if tech_repl not in metadata.keys():
                metadata[tech_repl] = {}
            if bio_repl not in metadata[tech_repl].keys():
                metadata[tech_repl][bio_repl] = {}
            metadata[tech_repl][bio_repl] = href
    for tech_repl in metadata.keys():
        for bio_repl in metadata[tech_repl].keys():
            print bio_repl
            href = __base_url__ + metadata[tech_repl][bio_repl]
            location = os.path.join(download_prefix, encode_id, "tech_repl_{}".format(tech_repl), "bio_repl_{}".format(bio_repl))
            os.makedirs(location)
            p = subprocess.call(["wget", "-c", href, "-P", location])

if __name__=="__main__":
    encode_downloader(sys.argv[1:])
