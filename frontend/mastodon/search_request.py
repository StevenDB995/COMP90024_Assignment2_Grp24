import requests


def search_accounts(start_time, end_time):
    url = f'http://127.0.0.1:9090/mastodon/accounts/search'
    params = {"start": start_time, "end": end_time}
    r = requests.get(url, params=params)
    print(r.text)


def search_statuses(tags, start_time, end_time):
    url = f'http://127.0.0.1:9090/mastodon/statuses/search/tags/{tags}'
    params = {"start": start_time, "end": end_time}
    r = requests.get(url, params=params)
    print(r.text)


def delete_accounts():
    url = f'http://127.0.0.1:9090/mastodon/accounts/delete'
    r = requests.delete(url)
    print(r.text)


def delete_statuses():
    url = f'http://127.0.0.1:9090/mastodon/statuses/delete'
    r = requests.delete(url)
    print(r.text)


if __name__ == '__main__':
    start_date = '2024-01-01'
    end_date = "2024-01-08"
    # tags_string = 'DomesticViolence&crime'
    tags_string = 'DomesticViolence'
    search_accounts(start_date, end_date)
