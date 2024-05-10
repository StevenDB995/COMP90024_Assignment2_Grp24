# API Documents

## Mastodon Data

### Harvest data

Mastodon accounts data:

```shell
curl -XPOST http://127.0.0.1:9090/mastodon/accounts/harvester/batch/{batch_num}
```

Mastodon statuses data:

```shell
curl -XPOST http://127.0.0.1:9090/mastodon/statuses/harvester/tags/{tags}/batch/{batch_num}
```

batch_num : The number of batches that the program harvests data from. 40 statuses are retrieved in each batch.

tags: Limit the harvested statuses tags. E.g: DomesticViolence, DomesticViolence&Female (multi-tags support)

### Search Data

Mastodon accounts data:

```shell
curl -XGET http://127.0.0.1:9090/mastodon/accounts/search?start={start_time}&end={end_time}
```

Mastodon statuses data:

```shell
curl -XGET http://127.0.0.1:9090/mastodon/statuses/search/tags/{tags}?start={start_time}&end={end_time}
```

Start time and end time must be in UTC format. E.g : '2024-05-08T05:00:00'

tags: Limit the statuses tags when searching. E.g: DomesticViolence, DomesticViolence&Female (multi-tags support)

### Delete Data

Mastodon accounts data:

```shell
curl -XDELETE http://127.0.0.1:9090/mastodon/accounts/delete
```

Mastodon statuses data:

```shell
curl -XDELETE http://127.0.0.1:9090/mastodon/statuses/delete
```