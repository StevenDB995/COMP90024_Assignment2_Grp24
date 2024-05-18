import requests


def search_accounts(field, gte, lte):
    url = f'http://127.0.0.1:9090/mastodon/accounts/search/field/{field}'
    params = {"gte": gte, "lte": lte}
    r = requests.get(url, params=params)
    print(r.text)


def search_statuses_tags(tags, field, gte, lte):
    url = f'http://127.0.0.1:9090/mastodon/statuses/search/tags/{tags}/field/{field}'
    params = {"gte": gte, "lte": lte}
    r = requests.get(url, params=params)
    print(r.text)


def search_statuses_public(field, gte, lte):
    url = f'http://127.0.0.1:9090/mastodon/statuses/search/public/field/{field}'
    params = {"gte": gte, "lte": lte}
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
    end_date = "2024-01-02"
    # tags_string = 'DomesticViolence&crime'
    tags_string = 'DomesticViolence'
    search_statuses_tags(tags_string, "created_at", start_date, end_date)
