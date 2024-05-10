from elasticsearch import Elasticsearch
import json

# Elasticsearch 客户端
es_client = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    basic_auth=("elastic", "elastic")
)

# 读取 JSON 数据并存入 Elasticsearch
def index_data(data):
    for record in data:
        es_client.index(index="weather_melbourne", body=record)

# 从大型 JSON 文件中逐批读取数据并存入 Elasticsearch
def process_large_json(json_file, batch_size=1000):
    with open(json_file) as f:
        data = json.load(f)
        total_records = len(data)
        batches = [data[i:i+batch_size] for i in range(0, total_records, batch_size)]
        for batch_num, batch in enumerate(batches):
            index_data(batch)
            print(f"Batch {batch_num+1}/{len(batches)} processed.")

# 指定 JSON 文件路径并调用函数
json_file_path = "WeatherObservations.json"
process_large_json(json_file_path)
