from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from urllib3 import disable_warnings, exceptions


def create_client():
    es_client = Elasticsearch(
        hosts="https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic")
    )
    return es_client


def sudo_data_search(index):
    disable_warnings(exceptions.InsecureRequestWarning)
    client = create_client()
    result = scan(client=client, index=index, scroll="1h")
    data = []
    for resp in result:
        data.append(resp["_source"])
    return {"status": "success", "data": data, "message": None}


def sudo_violence_search():
    return sudo_data_search('sudo_violence')
