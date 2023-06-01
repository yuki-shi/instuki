# instuki ~ scrape Instagram for benchmarking
extraction of public engagement data from Instagram profiles.

## :robot: use cases
basic diagnostic of the latest posts of one or more Instagram profiles, such as frequeny of posting and overall engagement.

## :steam_locomotive: usage

### getting sessionid
on a logged in Instagram session, open the developer tools and click on the *application* tab:


![](https://github.com/yuki-shi/instuki/blob/main/assets/session_id.png)




then select the URL under *cookies* and copy the string on *sessionid*


![](https://github.com/yuki-shi/instuki/blob/main/assets/session_id2.png)

### setup
create an environmental variable with the copied *sessionid*:
```bash
$ export SESSION_ID={session_id}
```

it's important to remember that when set this way, environmental variables aren't persistent!

### run
query for profile metrics by running the script with the *-u* argument followed by one or more usernames:
```bash
$ python3 main.py -u "{username_1, username_2}"
```


## :honeybee: troubleshooting

## :jack_o_lantern: technology
python.
