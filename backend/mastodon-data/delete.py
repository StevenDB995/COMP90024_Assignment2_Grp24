from elasticsearch import Elasticsearch, NotFoundError


def delete_index(index):
    es_client = Elasticsearch(
        hosts="https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic")
    )
    try:
        es_client.indices.delete(index=index)
        return {"status": "success", "data": {}, "message": None}
    except NotFoundError:
        return {"status": "failed", "data": {}, "message": "The target mastodon data has already been deleted"}


def accounts_delete():
    return delete_index("mastodon_accounts")


def statuses_delete():
    return delete_index("mastodon_statuses")
