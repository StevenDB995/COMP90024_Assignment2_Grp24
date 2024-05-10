import re
import json
from time import time, sleep
import requests
from elasticsearch import Elasticsearch, BadRequestError


def create_client():
    es_client = Elasticsearch(
        hosts="https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic")
    )
    return es_client


def accounts_process(toots, es_client, index):
    def data_process(user):
        wanted_keys = ['username', 'created_at', "followers_count", "following_count", "statuses_count",
                       "last_status_at"]
        user_info = dict()
        for k in wanted_keys:
            user_info[k] = user[k]
        return user_info

    for toot in toots:
        user_id = toot["account"]["id"]
        if es_client.exists(index=index, id=user_id):
            continue
        user_process = data_process(toot["account"])
        es_client.index(index=index, id=user_id, document=user_process)


def statuses_process(toots, es_client, index):
    def data_process(status):
        s = dict()
        s["created_at"] = status["created_at"]
        s["reblogs_count"] = status["reblogs_count"]
        s["favourites_count"] = status["favourites_count"]
        s["replies_count"] = status["replies_count"]
        re_obj = re.compile(r'<[^>]+>', re.S)
        s["content"] = re_obj.sub('', status["content"])
        tags = []
        if status['tags']:
            for t in status['tags']:
                tags.append(t['name'])
        s['tags'] = tags
        return s

    for toot in toots:
        if es_client.exists(index=index, id=toot["id"]):
            continue
        toot_process = data_process(toot)
        es_client.index(index=index, id=toot["id"], document=toot_process)


def timeline_search(host, tags, index, batch_size):
    params = {'limit': 40}
    if tags:
        hashtag = tags[0]
        api = f'/api/v1/timelines/tag/{hashtag}'
        params['any'] = tags[1:]
    else:
        api = '/api/v1/timelines/public'
    url = host + api

    es_client = create_client()
    try:
        es_client.indices.create(index=index)
    except BadRequestError:
        print("Index Already Exists")

    process_function = accounts_process if index == 'mastodon_accounts' else statuses_process

    i = 1
    status = 'success'
    message = None
    start_time = time()
    for i in range(1, batch_size + 1):
        # Mastodon's API rate limits per user account. By default, the limit is 300 requests per 5 minute time slot.
        if i % 300 == 0:
            now = time()
            if now - start_time < 300:
                sleep(300 - (now - start_time))
            start_time = time()

        r = requests.get(url, params=params)
        try:
            toots = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            status = 'Termination in advance'
            message = 'Json Decode Error: ' + json.decoder.JSONDecodeError.msg
            break

        if len(toots) == 0:
            status = 'Termination in advance'
            message = "No more data detected"
            break

        if isinstance(toots, dict) and 'error' in toots:
            status = 'Termination in advance'
            message = toots['error']
            break

        process_function(toots, es_client, index)

        max_id = toots[-1]['id']
        params['max_id'] = max_id

    return {"status": status, "data": {}, "message": message, 'batch_num': i}
