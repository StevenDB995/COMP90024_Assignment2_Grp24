import json
import os
import sys
from types import SimpleNamespace

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
# filepath = "/Users/macbookpro/Documents/COMP90024_CCC/Assignment2/COMP90024_Assignment2_Grp24/data/family_violence/csa_family_violence.csv"
import warnings
warnings.filterwarnings("ignore")


def main(filepath):
    es_client = Elasticsearch(
        "https://localhost:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic")
    )

    with open(filepath, "rb") as file:
        data = json.load(file)
    features = data['features']
    for idx in range(len(features)):
        dic_data = features[idx]['properties']
        print(dic_data)
        es_client.index(index="sudo_violence", body = dic_data)
        
    # bulk data into ES
    print(f"Finished processing data")


main(sys.argv[1])