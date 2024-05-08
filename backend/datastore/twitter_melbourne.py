import json
import os
import sys

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def gen_data(index, chunk):
    for doc in chunk:
        doc["_index"] = index
        yield doc


def main(filename):
    es_client = Elasticsearch(
        "https://localhost:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic")
    )

    file_size = os.path.getsize(filename)
    chunk_size = 10000000
    num_of_chunks = file_size // chunk_size + 1

    f = open(filename, "rb")

    # store data to es chunk by chunk
    for i in range(num_of_chunks):
        # processing a data chunk
        if i == num_of_chunks - 1:
            chunk_size = file_size % num_of_chunks

        read_size = 0
        chunk_data = []

        while read_size < chunk_size:
            line_bytes = f.readline()
            if not line_bytes:
                break
            line = line_bytes.decode()
            stripped_line = line.strip()
            trimmed_line = stripped_line[:-1] if stripped_line[-1] == ',' else stripped_line
            read_size += len(line_bytes)

            try:
                chunk_data.append(json.loads(trimmed_line))
            except json.JSONDecodeError:
                pass

        print(f"Processing chunk #{i} ...")
        num_added, errors = bulk(es_client, gen_data("twitter_melbourne", chunk_data))
        print(f"Finished processing chunk #{i}. Docs added: {num_added}, errors occurred: {len(errors)}")
        print(f"Progress: {i+1}/{num_of_chunks} chunks indexed")

    f.close()


main(sys.argv[1])
