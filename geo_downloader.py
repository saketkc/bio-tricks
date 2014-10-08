#!/usr/bin/env python
"""Script for automated downloading of
raw data from GEO database
Example:
    python geo_downloader.py --dfile dataset.md [From Methbase-tracker]
    python geo_downloader.py
"""

import csv
from Bio import Entrez
import os
import sys
from ftplib import FTP
import tempfile
import hashlib
import shutil
import argparse
from bs4 import BeautifulSoup
import yaml

__GEO_LINK_NAME__ = 'GSE Link'
__NCBI_FTP__ = 'ftp-trace.ncbi.nlm.nih.gov'
__GEO_LINK_COLUMN__ = 3
"""
Checks to run on NCBI output for a Geo project
Example: Ensure the results were generated from a Methylation experiment
{'gdsType': 'Methylation profiling by high throughput sequencing'}"""
__DATA_CHECKS__ = {}
# Absolute path where files are downloaded
__ROOT_DOWNLOAD_LOCATION__ = '/media/data2/'
__RETMAX__ = 10**9


class GEOQuery:
    def __init__(self, search_term, email="all@smithlabresearch.org"):
        Entrez.email = email
        # Geo Datasets database
        self.database = 'gds'
        # Refer http://www.ncbi.nlm.nih.gov/geo/info/qqtutorial.html
        # on how to search
        # For e.g. "Methylation profiling by high throughput sequencing"[DataSet Type] AND "Homo Sapiens"[Organism]
        # or "Methylation profiling by high throughput sequencing"[DataSet Type] AND "Mus Musculus"[Organism]
        self.search_term = search_term
        self.max_records = None

    def submit_query(self, retstart=0):
        """
        Submit Query to GEODatasets
        Returns records
        """
        query = Entrez.esearch(db=self.database, term=self.search_term, retmax=__RETMAX__, retstart=retstart)
        record = Entrez.read(query)
        if self.max_records is None:
            self.max_records = record['Count']
        return record

    def get_titles(self, uid_list=None):
        """
        Returns titles
        """
        query = Entrez.esummary(db=self.database, id=(",").join(uid_list))
        records = Entrez.read(query)
        return records

    def get_authors(self, pubmed_id_list):
        """Get authors form pubmed id list
        Data can exist without the publication having a pubmed id.
        So a more concrete way to store the data should be 'Contributor' field.
        """
        query = Entrez.esummary(db="pubmed", id=(",").join(pubmed_id_list))
        records = Entrez.read(query)
        return records

    def get_gsm_from_gse(self, geosample_id):
        # GDS = Geo DataSets
        #         ^
        #         |
        # GPL = Geo PLatform
        #         ^
        #         |
        # GSE = Geo Sample sEries
        #         ^
        #         |
        # GSM = Geo SaMple
        #         ^
        #         |
        #       Raw SRA

        # Get all GSM from each GSE
        query = Entrez.esearch(db='gds', term=geosample_id + " AND \"gsm\"", retmax=__RETMAX__)
        records = Entrez.read(query)
        return records

    def get_sra_from_gsm(self, gsm_id_list):
        """
        Get SRA links from GSM
        """
        query = Entrez.esummary(db='gds', id=(",").join(gsm_id_list))
        records = Entrez.read(query)
        return records

    def get_sra_metadata(self, sra_id):
        """Get SRA metadata"""
        query = Entrez.esearch('sra', term=sra_id)
        record = Entrez.read(query)
        query = Entrez.esummary(db='sra', id=record['IdList'])
        records = Entrez.read(query)
        return records


def stop_err(message):
     sys.stderr.write('ERROR: ' + message + '\n')
     sys.exit(1)


class MarkdownParser:

    """
    This class implements a very raw parser for parsing
    our markdown fikes. The current format used:

        |Project name|Content|GSE link|paper link|Method|Who|Finished|
        |:---:|:---:|:---:|:---:|:---:|:---:|:---:|

    The implementation assumes that the first occurence of '|' is a good enough
    catch to estimate the number of columns, then reads this line as its header
    and looks for the column number of 'GSE link'. The GEO links are then stored
    as a {'project_name': 'GEO accession key'}
    """

    def __init__(self, file_location):
        self.file_location = file_location
        assert(os.path.isfile(file_location))

    def is_row_junk(self, row):
        """
        Return True if a row has  at least one occurence of the  separator: ':---:'
        """
        if len(row) <= 7:
            return True
        for element in row:
            if element == ':---:':
                return True
        return False

    def get_geo_column_number(self, header_row):
        """
        Returns the column number where the __GEO_LINK_NAME__
        appears in the header row
        """
        for id, element in enumerate(header_row):
            if element == __GEO_LINK_NAME__:
                return id
        return None

    def get_header(self):
        """
        Moves the file pointer to next line till it encounters a header column as described in __init__
        """
        row = self.reader.next()
        while len(row) < 9:
            row = self.reader.next()
            if len(row) == 0:
                row = self.reader.next()
        return row

    def get_geo_links(self):
        """
        Returns a dictiornary with keys as the project name
        and values as the geo links
        """
        self.reader = csv.reader(open(self.file_location, 'r'), delimiter='|')
        header = self.get_header()
        assert(header is not None)
        column_number = __GEO_LINK_COLUMN__
        assert(column_number is not None)
        geo_links = {}
        for row in self.reader:
            if not self.is_row_junk(row):
                project_name = row[1]
                geo_link = row[column_number]
                geo_link = geo_link.split('=')
                try:
                    geo_link = geo_link[1]
                    geo_link = geo_link.replace(')', '')
                    geo_links[project_name] = geo_link
                except IndexError:
                    sys.stderr.write(
                        'ERROR parsing record for {} \n'.format(project_name))
        return geo_links


def is_already_downloaded(temp_file, download_to):
    """
    Checks if the SRA being downloaded is already present,
    """
    if os.path.isfile(download_to):
        return True
    return False

def safe_to_download(temp_file, download_to):
    """
    Verifies if the checksums are different[To ensure reproducubility]
    """
    if not os.path.isfile(download_to):
        return True
    existing_hash = hashlib.sha256(open(download_to, 'rb').read()).digest()
    moving_hash = hashlib.sha256(open(temp_file, 'rb').read()).digest()
    if existing_hash == moving_hash:
        return True
    else:
        return False

def download(download_location=None, sra=None, ncbi_ftp=None):
    """
    Pulls SRA from the FTP
    """
    if not os.path.exists(download_location):
        os.makedirs(download_location)
    temp_dir = tempfile.mkdtemp()
    download_to = os.path.join(download_location, sra)
    temp_file = os.path.join(temp_dir, sra)
    temp_write = open(temp_file, 'wb')
    ncbi_ftp.retrbinary('RETR {}'.format(sra), temp_write.write)
    temp_write.close()
    if is_already_downloaded(temp_file, download_to):
        print "WARNING: {} already present ".format(download_to)
        if safe_to_download(temp_file, download_to):
            shutil.move(temp_file, download_to)
        else:
            print sys.stderr.write("ERROR, file being overwritten fails checksum match: {} "
                                    .format(download_to))
    else:
        shutil.move(temp_file, download_to)
    print "Written: ", sra
    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    if __ROOT_DOWNLOAD_LOCATION__ == '':
        stop_err('__ROOT_DOWNLOAD_LOCATION__ not set')
    parser = argparse.ArgumentParser(
        description="Argument parser for downloading GEO files")
    parser.add_argument(
        '--dfile',
        type=str,
        help='Absolute path to markdown dataset file')
    args = parser.parse_args(sys.argv[1:])
    ncbi_ftp = FTP(__NCBI_FTP__)
    ncbi_ftp.login()
    temp_dir = tempfile.mkdtemp()
    if args.dfile:
        fs = MarkdownParser(args.dfile)
        geo_links = fs.get_geo_links()
        project_names = geo_links.keys()
        ids_to_download = [geo_links[key] for key in project_names]
    else:
        geoQ = GEOQuery("\"Methylation profiling by high throughput sequencing\"[DataSet Type]")
        records = geoQ.submit_query()
        id_list = records['IdList']
        records = geoQ.get_titles(id_list)
        for i, record in enumerate(records):
            print "{}: {}: {}".format(i+1, record['Accession'].encode('utf-8'), record['title'].encode('utf-8'))
        print("Enter 0 to download all(Warning!)\n"
            "Enter 1-3 to download datasets from 1-3\n"
            "Enter GSE25836, GSE47752 to download GSE25836 and GSE47752")
        to_download = raw_input("")
        to_download = to_download.replace(" ", "")
        if "-" in to_download:
            split = to_download.split('-')
            start = int(split[0])-1
            if split[1]=="":
                end = len(records)-1
            else:
                end = int(split[1])-1
            range_to_download = range(start, end+1)
            ids_to_download = [records['Accession'].encode('utf-8') for i, record in enumerate(records) if i in range_to_download]
        elif "GSE" in to_download:
            ids_to_download = to_download.split(',')
        elif to_download == "0":
            ids_to_download = [records['Accession'].encode('utf-8') for i, record in enumerate(records)]
    Samples = {}
    for gse_id in ids_to_download:
        gse_location = os.path.join(__ROOT_DOWNLOAD_LOCATION__, gse_id)
        if not os.path.exists(gse_location):
            os.makedirs(gse_location)
        else:
            sys.stderr.write("WARNING: {} location already exists".format(gse_location))
        gsm_records = geoQ.get_gsm_from_gse(gse_id)
        id_list = gsm_records['IdList']
        sra_records = geoQ.get_sra_from_gsm(id_list)
        for sra_record in sra_records:
            ext_relations = sra_record['ExtRelations']
            sra_title = sra_record['title'].replace(" ", "__") + "___" + sra_record['Accession']
            gsm_location = os.path.join(gse_location, sra_title)
            if not os.path.exists(gsm_location):
                os.makedirs(gsm_location)
            sra_links = filter(lambda x: x['RelationType']=='SRA', ext_relations)
            assert(len(sra_links) == 1)
            target_ftp_link = sra_links[0]['TargetFTPLink']
            ncbi_ftp.cwd("/")
            ncbi_ftp.cwd(target_ftp_link[32:])
            sra_ids = ncbi_ftp.nlst()
            if len(sra_ids) > 1:
                print "Found technical replicates at", target_ftp_link
                for replicate_count, sra_id in enumerate(sra_ids):
                    replicate_location = os.path.join(gsm_location, sra_title + "___R" + str(replicate_count+1))
                    ncbi_ftp.cwd(sra_id)
                    sra_file = ncbi_ftp.nlst()[0]
                    download(replicate_location, sra_file, ncbi_ftp)
                    metadata = geoQ.get_sra_metadata(sra_id)
                    strategy = str(BeautifulSoup(metadata[0]['ExpXml']).find('library_strategy').string)
                    Samples[str(sra_title) + "___R" + str(replicate_count+1)] = {'Path' : str(os.path.join(replicate_location, sra_id, ".sra")), 'Strategy': strategy}
                    ncbi_ftp.cwd("../")
            else:
                sra_id = sra_ids[0]
                ncbi_ftp.cwd(sra_id)
                assert(len(ncbi_ftp.nlst()) == 1)
                sra_file = ncbi_ftp.nlst()[0]
                metadata = geoQ.get_sra_metadata(sra_id)
                strategy = str(BeautifulSoup(metadata[0]['ExpXml']).find('library_strategy').string)
                Samples[sra_title] = {'Path': str(os.path.join(gsm_location, sra_id, ".sra")), 'Strategy': strategy}
                download(gsm_location, sra_file, ncbi_ftp)
        with open('result.yml', 'w') as yaml_file:
            yaml_file.write( yaml.dump(Samples, default_flow_style=False))
