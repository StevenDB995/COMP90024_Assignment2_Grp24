# API Documents

## Mastodon Data

### Harvest data

Mastodon accounts data:

```shell
curl -H "Content-Type:application/json" --data '{"batch": {batch_num}, "max_id": {max_id}}' -XPOST http://127.0.0.1:9090/mastodon/accounts/harvester
```

```shell
curl -H "Content-Type:application/json" --data '{"batch": {batch_num}, "tags": {tags}, "max_id": {max_id}}' -XPOST http://127.0.0.1:9090/mastodon/statuses/harvester
```

batch_num : The number of batches that the program harvests data from. 40 statuses are retrieved in each batch.

tags: Limit the harvested statuses tags. E.g: DomesticViolence, DomesticViolence&Female (multi-tags support)

max_id: All results returned will be lesser than this ID. In effect, sets an upper bound on results.

### Search Data

Mastodon accounts data:

```shell
curl -XGET http://127.0.0.1:9090/mastodon/accounts/search?start={start_time}&end={end_time}
```

Mastodon statuses data:

```shell
curl -XGET http://127.0.0.1:9090/mastodon/statuses/search/public?start={start_time}&end={end_time}
```

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
