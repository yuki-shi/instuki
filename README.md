# instuki: yet another instagram scraper
extraction of public engagement data from Instagram profiles.

## :robot: use cases
basic diagnostic of the latest posts of an Instagram profile, such as frequeny of posting and overall engagement.

## :steam_locomotive: usage

### getting sessionid
on a logged in Instagram session, open the developer tools and click on the *application* tab:


![Captura de tela de 2023-05-25 16-38-34](https://github.com/yuki-shi/instuki/assets/88805836/2e2f32fa-d10b-4b60-ae2f-96075dccbcfb)




then select the URL under *cookies* and copy the string on *sessionid*


![Captura de tela de 2023-05-25 16-38-44](https://github.com/yuki-shi/instuki/assets/88805836/664254de-0428-48f4-baaa-fb57bb780919)

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




## :jack_o_lantern: technology
python.
