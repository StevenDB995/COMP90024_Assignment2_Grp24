import requests


def search_test():
    start_time = '2024-05-08T05:00:00'
    end_time = "2024-05-08T09:00:00"
    url = f'http://127.0.0.1:9090/mastodon/accounts/search'
    params = {"start": start_time, "end": end_time}
    r = requests.get(url, params=params)
    print(r.text)


def delete_test():
    url = f'http://127.0.0.1:9090/mastodon/accounts/delete'
    r = requests.delete(url)
    print(r.text)


if __name__ == '__main__':
    delete_test()
