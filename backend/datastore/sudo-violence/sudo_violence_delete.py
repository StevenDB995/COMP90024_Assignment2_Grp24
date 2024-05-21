from elasticsearch import Elasticsearch


def delete():
    try: 
        es_client = Elasticsearch(
            "https://localhost:9200",
            verify_certs=False,
            basic_auth=("elastic", "elastic")
        )

        es_client.indices.delete(index="sudo_violence")
        return "successful"
    except Exception as e:
        print(f"Failed to connect to Elasticsearch: {e}")
        return