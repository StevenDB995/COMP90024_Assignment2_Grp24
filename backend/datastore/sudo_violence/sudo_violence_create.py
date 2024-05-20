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
        "lga_name11": {
            "type": "text"
        },"affected_family_members_rate_per_100k_2017_18":{
            "type":"float"
        },
        "lga_code11": {
            "type": "text"
        },
        "affected_family_members_rate_per_100k_2014_15":{
            "type":"float"
        },
        "affected_family_members_rate_per_100k_2015_16":{
            "type":"float"
        },
        "affected_family_members_rate_per_100k_2016_17":{
            "type":"float"
        },
        "affected_family_members_rate_per_100k_2013_14":{
            "type":"float"
        }

    }
}

es_client.indices.create(index="sudo_violence", settings=settings, mappings=mappings)
