from harvest_util import *
from flask import request
from urllib3 import disable_warnings, exceptions


def data_harvester(index):
    disable_warnings(exceptions.InsecureRequestWarning)
    host = 'https://mastodon.au'
    data = request.get_json()
    if data is None:
        return {"status": "failed", "data": {}, "message": "Params not provided"}
    batch_size = data.get("batch")
    tags = data.get("tags")
    max_id = data.get("max_id")
    if tags:
        tags = tags.lower()
        tags = tags.split("&")
    else:
        tags = []
    if type(batch_size) != int:
        return {"status": "failed", "data": {}, "message": "Incorrect batch quantity or batch quantity not provided"}
    return timeline_search(host, tags, index, batch_size, max_id)


def accounts_harvester():
    return data_harvester('mastodon_accounts')


def statuses_harvester():
    return data_harvester('mastodon_statuses')
