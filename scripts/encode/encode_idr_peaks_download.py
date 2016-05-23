import requests

__base_url__ = 'https://www.encodeproject.org/'

ALLOWED_FILETYPES = ['bed narrowPeak', 'bed broadPeak']

def get_experiment(experiment_id):
    """Get and save metadata for an experiment"""
    req = requests.get("{}experiments/{}/?format=json".format(__base_url__, experiment_id))
    metadata = req.json()
    return metadata

def filter_metadata(metadata,
                    filter_dict={'files.output_type': 'optimal idr thresholded peaks'}):
    """Can think of supporting one nested key for now"""
    filter_keys = filter_dict.keys()[0].split('.')
    value = filter_dict.values()[0]
    files = metadata['files']
    filter_records = []
    for f in files:
        file_status = f['status']
        file_type = f['file_type']
        #output_type = f['output_type']
        filter_1 = f[filter_keys[0]]
        filter_2 = f[filter_keys[1]]
        if filter_2 == value and file_type in ALLOWED_FILETYPES and file_status == 'released':
            dataset = f['dataset']
            dataset = dataset.replace('experiments','').replace('/','')
            href = f['href']
            title = f['title']
            assembly = f['assembly']
            print dataset
            filter_records.append({'href': href,
                                   'metadata':f,
                                   'parent_metadata': metadata,
                                   'dataset': dataset,
                                   'peakfilename': title,
                                   'file_type': file_type,
                                   'file_status': file_status,
                                   'assembly': assembly})
    return filter_records

def search_encode_tfs():
    url = __base_url__ + '/search?type=Experiment&assay_title=ChIP-seq&limit=all&status=released&target.investigated_as=transcription+factor&format=json'
    req = requests.get(url)
    resp_json = req.json()
    all_samples = resp_json['@graph']
    all_tfs = [sample['target']['label'] for sample in all_samples]
    all_tfs =  set(all_tfs)
    all_experiments = [sample['@id'].strip().replace('/','').replace('experiments', '') for sample in all_samples]
    for experiment in all_experiments:
        expt_metadata = get_experiment(experiment)
        filter_metadata(expt_metadata)
if __name__ == '__main__':
    search_encode_tfs()
