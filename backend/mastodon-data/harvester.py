from harvest_util import *
from flask import request
from urllib3 import disable_warnings, exceptions


def accounts_harvester():
    disable_warnings(exceptions.InsecureRequestWarning)
    host = 'https://mastodon.au'
    try:
        batch_size = request.headers.get("X-Fission-Params-Batch")
        batch_size = int(batch_size)
    except (TypeError, ValueError):
        return {"status": "failed", "data": {}, "message": "Incorrect URL"}
    timeline_search(host, [], extract_accounts_info, batch_size)
    return {"status": "success", "data": {}, "message": None}


def statuses_harvester():
    disable_warnings(exceptions.InsecureRequestWarning)
    host = 'https://mastodon.au'
    try:
        tags = request.headers.get("X-Fission-Params-Tags")
        tags = tags.split("&")
        batch_size = request.headers.get("X-Fission-Params-Batch")
        batch_size = int(batch_size)
    except (TypeError, ValueError, AttributeError):
        return {"status": "failed", "data": {}, "message": "Incorrect URL"}
    timeline_search(host, tags, extract_tweets_info, batch_size)
    return {"status": "success", "data": {}, "message": None}
