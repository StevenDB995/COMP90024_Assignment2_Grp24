from elasticsearch import Elasticsearch

es_client = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    basic_auth=("elastic", "elastic")
)

settings = {
    "index": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    }
}

mappings = {
    "properties": {
        "created_at": {
            "type": "date"
        },
        "text": {
            "type": "text"
        },
        "sentiment": {
            "type": "float"
        },
        "location": {
            "type": "text"
        }
    }
}

es_client.indices.create(index="twitter_melbourne", settings=settings, mappings=mappings)
