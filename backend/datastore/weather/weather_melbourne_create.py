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
        "Minimum temperature (°C)": {"type": "float"},
        "Maximum temperature (°C)": {"type": "float"},
        "Rainfall (mm)": {"type": "float"},
        "Evaporation (mm)": {"type": "float"},
        "Sunshine (hours)": {"type": "float"},
        "Direction of maximum wind gust": {"type": "keyword"},
        "Speed of maximum wind gust (km/h)": {"type": "integer"},
        "Time of maximum wind gust": {"type": "keyword"},
        "9am Temperature (°C)": {"type": "float"},
        "9am relative humidity (%)": {"type": "integer"},
        "9am cloud amount (oktas)": {"type": "integer"},
        "9am wind direction": {"type": "keyword"},
        "9am wind speed (km/h)": {"type": "integer"},
        "9am MSL pressure (hPa)": {"type": "float"},
        "3pm Temperature (°C)": {"type": "float"},
        "3pm relative humidity (%)": {"type": "integer"},
        "3pm cloud amount (oktas)": {"type": "integer"},
        "3pm wind direction": {"type": "keyword"},
        "3pm wind speed (km/h)": {"type": "integer"},
        "3pm MSL pressure (hPa)": {"type": "float"}
    }
}

es_client.indices.create(index="weather_melbourne", settings=settings, mappings=mappings)
