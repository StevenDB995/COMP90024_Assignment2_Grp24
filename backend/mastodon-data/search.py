import elasticsearch
from flask import request
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


def data_search(index):
    disable_warnings(exceptions.InsecureRequestWarning)
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    query = {
        "query": {
            "range": {'created_at': {"gte": start_time, "lte": end_time}}
        }
    }
    client = create_client()
    try:
        result = scan(client=client, index=index, query=query, scroll="1h")
        data = []
        for resp in result:
            data.append(resp["_source"])
        return {"status": "success", "data": data, "message": None}
    except elasticsearch.NotFoundError:
        return {"status": "failed", "data": {}, "message": "There is no that mastodon data yet"}
    except elasticsearch.BadRequestError:
        return {"status": "failed", "data": {}, "message": "The start or end time are not in UTC format"}


def accounts_search():
    return data_search('mastodon_accounts')


def statuses_search():
    return data_search('mastodon_statuses')
