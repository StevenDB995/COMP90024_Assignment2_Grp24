import re
import json
import requests
from elasticsearch import Elasticsearch, BadRequestError


def create_client():
    es_client = Elasticsearch(
        hosts="https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic")
    )
    return es_client


def gather_user_info(user):
    wanted_keys = ['username', 'created_at', "followers_count", "following_count", "statuses_count", "last_status_at"]
    user_info = dict()
    for k in wanted_keys:
        user_info[k] = user[k]
    return user_info


def statuses_process(status):
    re_obj = re.compile(r'<[^>]+>', re.S)
    s = dict()
    s["created_at"] = status["created_at"]
    s["content"] = re_obj.sub('', status["content"])
    tags = []
    if status['tags']:
        for t in status['tags']:
            tags.append(t['name'])
    s['tags'] = tags
    return s


def timeline_search(host, tags, data_extract, batch_size):
    params = {'limit': 40}
    if tags:
        hashtag = tags[0]
        api = f'/api/v1/timelines/tag/{hashtag}'
        params['any'] = tags[1:]
    else:
        api = '/api/v1/timelines/public'
    data_extract(host, api, params, batch_size)


def extract_tweets_info(host, api, params, batch_size):
    url = host + api
    index = 'mastodon_statuses'
    es_client = create_client()
    try:
        es_client.indices.create(index=index)
    except BadRequestError:
        print("Index Already Exists")

    for i in range(batch_size):
        r = requests.get(url, params=params)
        try:
            toots = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print(r.status_code)
            break

        if len(toots) == 0:
            break

        if isinstance(toots, dict) and 'error' in toots:
            print(toots['error'])
            break

        for toot in toots:
            if es_client.exists(index=index, id=toot["id"]):
                continue
            toot_process = statuses_process(toot)
            es_client.index(index=index, id=toot["id"], document=toot_process)

        max_id = toots[-1]['id']
        params['max_id'] = max_id


def extract_accounts_info(host, api, params, batch_size):
    url = host + api
    index = 'mastodon_accounts'
    es_client = create_client()
    try:
        es_client.indices.create(index=index)
    except BadRequestError:
        print("Index Already Exists")

    for i in range(batch_size):
        r = requests.get(url, params=params)
        try:
            toots = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print(r.status_code)
            break

        if len(toots) == 0:
            break

        if isinstance(toots, dict) and 'error' in toots:
            print(toots['error'])
            break

        for toot in toots:
            user_id = toot["account"]["id"]
            if es_client.exists(index=index, id=user_id):
                continue
            user_info = gather_user_info(toot["account"])
            es_client.index(index=index, id=user_id, document=user_info)

        max_id = toots[-1]['id']
        params['max_id'] = max_id
