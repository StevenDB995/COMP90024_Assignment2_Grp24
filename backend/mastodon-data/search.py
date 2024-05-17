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


def data_search(index, has_tags=False):
    disable_warnings(exceptions.InsecureRequestWarning)
    field = request.headers.get("X-Fission-Params-Field")
    gte = request.args.get("gte")
    lte = request.args.get("lte")
    term_query = []
    if has_tags:
        tags = request.headers.get("X-Fission-Params-Tags")
        if tags is None:
            return {"status": "failed", "data": {}, "message": "Incorrect URL"}
        tags = tags.lower().split('&')
        for tag in tags:
            term_query.append({"term": {"tags": tag}})
    query = {
        "query": {
            "bool": {
                "filter": [
                    {"range": {field: {"gte": gte, "lte": lte}}}
                ] + term_query
            }
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
        return {"status": "failed", "data": {}, "message": "Incorrect gte or lte parameters format"}


def accounts_search():
    return data_search('mastodon_accounts')


def statuses_search_public():
    return data_search('mastodon_statuses')


def statuses_search_tags():
    return data_search('mastodon_statuses', has_tags=True)
