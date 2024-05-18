import json
import pandas as pd
from elasticsearch import Elasticsearch
from collections import defaultdict
import time

def fetch_data_for_month(es_client, index, month_start, month_end, size=1000):
    query_body = {
        "query": {
            "range": {
                "created_at": {
                    "gte": month_start,
                    "lt": month_end
                }
            }
        },
        "size": size
    }
    response = es_client.search(index=index, body=query_body)
    return response['hits']['hits']

def fetch_twitter_data(es_client):
    # Define monthly time ranges
    monthly_sentiments = defaultdict(list)
    for year in range(2021, 2023):  # Assuming data is from 2021 to 2022
        for month in range(1, 13):
            month_start = f"{year}-{month:02d}-01T00:00:00.000Z"
            if month == 12:
                month_end = f"{year+1}-01-01T00:00:00.000Z"
            else:
                month_end = f"{year}-{month+1:02d}-01T00:00:00.000Z"

            # Fetch data for the month
            monthly_data = fetch_data_for_month(es_client, "twitter_melbourne", month_start, month_end)
            for hit in monthly_data:
                source = hit['_source']
                sentiment = source['sentiment']
                monthly_sentiments[f"{year}-{month:02d}"].append(sentiment)

    # Calculate average sentiment for each month
    average_monthly_sentiments = {month: sum(sentiments) / len(sentiments) for month, sentiments in monthly_sentiments.items()}
    return average_monthly_sentiments

def main():
    try:
        # Record start time
        start_time = time.time()

        # Create Elasticsearch client
        es_client = Elasticsearch(
            "https://elasticsearch-master.elastic.svc.cluster.local:9200",
            verify_certs=False,
            basic_auth=("elastic", "elastic")
        )

        # Query weather data
        weather_query_body = {
            "query": {
                "range": {
                    "Date": {
                        "gte": "2021-06-01",
                        "lt": "2022-07-01"
                    }
                }
            },
            "size": 9000
        }

        # Execute query
        weather_result = es_client.search(index="weather_melbourne", body=weather_query_body)

        # Process weather data query results
        weather_data = [hit['_source'] for hit in weather_result['hits']['hits']]
        weather_df = pd.DataFrame(weather_data)

        # Ensure the Date column is in datetime format
        weather_df['Date'] = pd.to_datetime(weather_df['Date'], errors='coerce')

        # Extract year and month
        weather_df['YearMonth'] = weather_df['Date'].dt.to_period('M').astype(str)

        # Calculate monthly weather averages
        monthly_weather_avg = weather_df.groupby('YearMonth').agg({
            'Rainfall (mm)': 'mean',
            'Sunshine (hours)': 'mean',
            'Speed of maximum wind gust (km/h)': 'mean'
        }).reset_index()

        # Fetch Twitter data
        average_monthly_sentiments = fetch_twitter_data(es_client)

        # Add average sentiment to monthly weather data
        monthly_weather_avg['Sentiment'] = monthly_weather_avg['YearMonth'].map(average_monthly_sentiments)

        # Fill missing sentiment values with None
        monthly_weather_avg['Sentiment'] = monthly_weather_avg['Sentiment'].apply(lambda x: x if pd.notnull(x) else None)

        # Convert to dictionary
        monthly_avg_dict = monthly_weather_avg.to_dict(orient='records')

        # Convert to JSON
        monthly_avg_json = json.dumps(monthly_avg_dict, default=str)

        # Record end time
        end_time = time.time()

        # Calculate execution time
        execution_time = end_time - start_time
        print(f'Execution time: {execution_time} seconds')

        return monthly_avg_json
    except Exception as e:
        return json.dumps({"error": str(e)})

