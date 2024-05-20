import json
import sys
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException


def main(filepath):
    # connect to Elastic search
    try: 
        es_client = Elasticsearch(
            "https://localhost:9200",
            verify_certs=False,
            basic_auth=("elastic", "elastic")
        )
    except Exception as e:
        print(f"Failed to connect to Elasticsearch: {e}")
        return  
    
    # open file 
    try: 
        with open(filepath, "rb") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: The file was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode the file as JSON.")
        return
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        return
    

    # upload file to elsatisc search
    features = data.get('features', [])
    for idx in range(len(features)):
        try: 
            dic_data = features[idx]['properties']
            es_client.index(index="sudo_violence", body = dic_data)
        
        except KeyError:
            print(f"Error: 'properties' key not found in data at index {idx}.")
        except ElasticsearchException as e:
            print(f"Error indexing data in Elasticsearch at index {idx}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing data at index {idx}: {e}")
 
    # finished uploading
    print(f"Finished processing data and storing data into Elastic Search")


main(sys.argv[1])