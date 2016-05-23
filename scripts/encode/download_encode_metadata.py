#!/usr/bin/env python
"""Download encode metadata to a MongoDB instance"""
import requests
from pymongo import MongoClient

collection_name = 'tf_metadata_05222016'
__base_url__ = 'https://www.encodeproject.org/'

def save_metadata(metadata):
    """Save metadata to mongodb"""
    client = MongoClient()
    db = client.moca_encode_tf
    result = db[collection_name].insert_one(metadata)

def get_experiment(experiment_id):
    """Get and save metadata for an experiment"""
    req = requests.get("{}experiments/{}/?format=json".format(__base_url__, experiment_id))
    metadata = req.json()
    if metadata['status'] != 'error':
        save_metadata(metadata)
    else:
        print 'Error fetching metadata for {}'.format(experiment_id)

def search_encode_tfs():
    url = __base_url__ + '/search?type=Experiment&assay_title=ChIP-seq&limit=all&status=released&target.investigated_as=transcription+factor&format=json'
    req = requests.get(url)
    resp_json = req.json()
    all_samples = resp_json['@graph']
    all_tfs = [sample['target']['label'] for sample in all_samples]
    all_tfs =  set(all_tfs)
    all_experiments = [sample['@id'].strip().replace('/','').replace('experiments', '') for sample in all_samples]
    for experiment in all_experiments:
        get_experiment(experiment)

if __name__ == '__main__':
    search_encode_tfs()

