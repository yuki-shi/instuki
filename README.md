# instuki: yet another instagram scraper
extraction of public engagement data from Instagram profiles.

## use cases
basic diagnostic of the latest posts of an Instagram profile, such as frequeny of posting and overall engagement.

## usage
create an enviromental variable with the session id cookie:
```bash
$ export SESSION_ID={session_id}
```
then query for username(s) metrics:
```bash
$ python3 main.py -u "{username_1, username_2}"
```

## technology
python.
