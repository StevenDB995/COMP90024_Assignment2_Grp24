from harvest_util import *
from flask import request
from urllib3 import disable_warnings, exceptions


def data_harvester(index, has_tags=False):
    disable_warnings(exceptions.InsecureRequestWarning)
    host = 'https://mastodon.au'
    try:
        if has_tags:
            tags = request.headers.get("X-Fission-Params-Tags")
            tags = tags.split("&")
        else:
            tags = []
        batch_size = request.headers.get("X-Fission-Params-Batch")
        batch_size = int(batch_size)
    except (TypeError, ValueError, AttributeError):
        return {"status": "failed", "data": {}, "message": "Incorrect URL"}
    return timeline_search(host, tags, index, batch_size)


def accounts_harvester():
    data_harvester('mastodon_accounts', has_tags=False)


def statuses_harvester_public():
    data_harvester('mastodon_statuses', has_tags=False)


def statuses_harvester_tags():
    data_harvester('mastodon_statuses', has_tags=True)
