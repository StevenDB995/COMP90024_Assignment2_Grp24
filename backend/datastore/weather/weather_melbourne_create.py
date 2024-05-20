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
        "Date": {"type": "date"},
        "Rainfall (mm)": {"type": "float"},
        "Sunshine (hours)": {"type": "float"},
        "Speed of maximum wind gust (km/h)": {"type": "integer"}
    }
}

es_client.indices.create(index="weather_melbourne", settings=settings, mappings=mappings)
