import requests


def harvest_statuses(tags, batch_size, max_id=None):
    # get 0.4MB data and earliest date is 2022-03-29 when batch_size=100, estimate batch_seize = (100 * 12500)
    url = f'http://127.0.0.1:9090/mastodon/statuses/harvester'
    r = requests.post(url, json={"tags": tags, "batch": batch_size, 'max_id': max_id})
    print(r.text)


def harvest_accounts(batch_size, max_id=None):
    # get 0.45MB data when batch_size=100, estimate batch_size = 100 * 12000
    url = f'http://127.0.0.1:9090/mastodon/accounts/harvester'
    r = requests.post(url, json={"batch": batch_size, 'max_id': max_id})
    print(r.text)


if __name__ == '__main__':
    # batch = 100 * 12000
    # upper = '111655536032787694'
    # harvest_accounts(batch, upper)
    harvest_statuses("DomesticViolence", 100 * 12500)
