from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import datetime as dt

def get_permalinks(page_source_path: str) -> list:
  with open(page_source_path, 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

  posts = soup.find_all('div', class_='_aabd')
  permalinks = []

  for post in posts:
    permalinks.append(f"https://www.instagram.com{post.find_all('a')[0]['href']}?__a=1&__d=dis")

  return permalinks

def get_post_metrics(post_permalink: str) -> dict:
  try:
    response = requests.get(post_permalink, cookies=cookies)
    response.raise_for_status()
  except requests.exceptions.HTTPError as error:
    raise SystemExit(error)
  
  post_data = json.loads(response.text)['items'][0]

  post_metrics = {
    'taken_at': post_data['taken_at'],
    'comment_count': post_data['comment_count'],
    'like_count': post_data['like_count']
  }

  return post_metrics

def timestamp_to_datetime(timestamp:int) -> dt.datetime:
  return dt.datetime.utcfromtimestamp(timestamp)

  
permalinks = get_permalinks('./pg_source.html')
#TODO: tornar sessionid variável de ambiente
cookies = {'sessionid': 'xxx'}
output_dict = {}

for permalink in permalinks:
  output_dict[permalink] = get_post_metrics(permalink)

df = (pd.DataFrame(output_dict)
        .transpose()
        .reset_index(names='permalink'))

df['taken_at'].apply(lambda x: timestamp_to_datetime(x))
#TODO: checar o timezone, talvez alterar para UTC-3

df.to_csv('ig_data.csv', index=False)