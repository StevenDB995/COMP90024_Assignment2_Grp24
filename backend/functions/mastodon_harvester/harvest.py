import json
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from mastodon import Mastodon


def gen_data(statuses):
    for doc in statuses:
        doc["_index"] = "statuses"
        yield doc


def main():
    start = time.time()
    m = Mastodon(api_base_url="https://mastodon.au")

    last_id = m.timeline(timeline="public", limit=1, remote=True)[0]["id"]
    time.sleep(30)
    statuses = m.timeline(timeline="public", since_id=last_id, remote=True)

    es_client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic")
    )

    result = bulk(es_client, gen_data(statuses))
    end = time.time()

    if len(result[1]) == 0:
        return {
            "status": "ok",
            "number_of_harvested_statuses": result[0],
            "duration": f"{end - start}s"
        }
    else:
        return json.dumps(result[1], default=str)
