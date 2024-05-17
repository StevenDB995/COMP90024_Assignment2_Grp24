from elasticsearch import Elasticsearch

es_client = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    basic_auth=("elastic", "elastic")
)

es_client.indices.delete(index="twitter_melbourne")
