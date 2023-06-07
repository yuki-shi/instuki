<body>
  <div align="center">
    <img src="https://github.com/yuki-shi/instuki/blob/main/assets/rainbow_catto.gif" width="8%">
    <h1>instuki ~ scrape Instagram for benchmarking</h1>
    <p>extraction of public engagement data from Instagram profiles.</p>
  </div>
  <h2>:robot: use cases</h2>
  <p>basic diagnostic of the latest posts of one or more Instagram profiles, such as frequeny of posting and overall engagement.</p>
  <h2>:steam_locomotive: usage</h2>
  <h3>getting sessionid</h3>
  <p>on a logged in Instagram session, open the developer tools and click on the <i>application</i> tab:</p>
  <img src="https://github.com/yuki-shi/instuki/blob/main/assets/session_id.png">
  <br>
  <p>then select the URL under <i>cookies</i> and copy the string on <i>sessionid</i></p>
  <img src="https://github.com/yuki-shi/instuki/blob/main/assets/session_id2.png">
  
  <h3>setup</h3>
  <p>create an environmental variable with the copied <i>sessionid</i>:
  
```bash
$ export SESSION_ID={session_id}
```
   it's important to remember that when set this way, environmental variables aren't persistent!</p>

  <h3>run</h3>
  <p>query for profile metrics by running the script with the <i>-u</i> argument followed by one or more usernames:
    
```bash
$ python3 main.py -u "{username_1, username_2}"
```
  </p>

  <h2>:honeybee: troubleshooting</h2>

  <h2>:jack_o_lantern: technology</h2>
  <p>python.</p>
</body>
