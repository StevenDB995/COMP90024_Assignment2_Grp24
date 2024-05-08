import requests


def harvest_statuses(tags, batch_size):
    # get 0.4MB data and earliest date is 2022-03-29 when batch_size=100, estimate batch_seize = (100 * 12500)
    url = f'http://127.0.0.1:9090/mastodon/statuses/harvester/tags/{tags}/batch/{batch_size}'
    r = requests.post(url)
    print(r.text)


def harvest_accounts(batch_size):
    # get 0.45MB data when batch_size=100, estimate batch_size = 100 * 12000
    url = f'http://127.0.0.1:9090/mastodon/accounts/harvester/batch/{batch_size}'
    r = requests.post(url)
    print(r.text)


if __name__ == '__main__':
    harvest_accounts(100 * 12000)
