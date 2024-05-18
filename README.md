# API Documents

## Mastodon Data

### Mastodon Accounts Data

#### Harvester:

```shell
curl -H "Content-Type:application/json" \
  --data '{"batch": {batch_num}, "max_id": {max_id}}' \
  -XPOST http://127.0.0.1:9090/mastodon/accounts/harvester
```

batch_num : The number of batches that the program harvests data from. 40 statuses are retrieved in each batch.

max_id: All results returned will be lesser than this ID. In effect, sets an upper bound on results.


#### Search:

```shell
curl -XGET http://127.0.0.1:9090/mastodon/accounts/search/field/{field}?gte={gte_value}&lte={lte_value}
```

gte stands for "greater than or equal to"

lte stands for "less than or equal to." 

It filter the mastodon data within the specified field range.


#### Delete:

```shell
curl -XDELETE http://127.0.0.1:9090/mastodon/accounts
```


### Mastodon Statuses Data

#### Harvester:

```shell
curl -H "Content-Type:application/json" \
  --data '{"batch": {batch_num}, "tags": {tags}, "max_id": {max_id}}' \
  -XPOST http://127.0.0.1:9090/mastodon/statuses/harvester
```

batch_num : The number of batches that the program harvests data from. 40 statuses are retrieved in each batch.

tags: Limit the harvested statuses tags. E.g: DomesticViolence, DomesticViolence&Female (multi-tags support)

max_id: All results returned will be lesser than this ID. In effect, sets an upper bound on results.


#### Search:

```shell
curl -XGET http://127.0.0.1:9090/mastodon/statuses/search/tags/{tags}/field/{field}?gte={gte_value}&lte={lte_value}
```

```shell
curl -XGET http://127.0.0.1:9090/mastodon/statuses/search/public/field/{field}?gte={gte_value}&lte={lte_value}
```

tags: Limit the statuses tags when searching. E.g: DomesticViolence, DomesticViolence&Female (multi-tags support)

gte stands for "greater than or equal to"

lte stands for "less than or equal to." 

It filter the mastodon data within the specified field range.


#### Delete:

```shell
curl -XDELETE http://127.0.0.1:9090/mastodon/statuses
```

## Sudo Data

### Sudo Violence Data

#### Search

```shell
curl -XGET http://127.0.0.1:9090/sudo/violence/search
```

## Twitter Data

#### Search

```shell
curl -XGET http://127.0.0.1:9090/twitter/search/field/{field}?gte={gte_value}&lte={lte_value}
```

gte stands for "greater than or equal to"

lte stands for "less than or equal to." 

It filter the mastodon data within the specified field range.

#### Delete:

```shell
curl -XDELETE http://127.0.0.1:9090/twitter
```