from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
from utils import timestamp_to_datetime


class InstukiScraper():
  def __init__(self, session_id, username):
    self.session_id = session_id
    self.username = username
    self.driver = self.init_driver()

  def init_driver(self) -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://www.instagram.com/{self.username}')
    driver.add_cookie({'name': 'sessionid', 'value': self.session_id})
    driver.get(f'https://www.instagram.com/{self.username}')

    # Check if the first post thumbnail is visible
    try:
      sleep(10)
      driver.find_element(By.CSS_SELECTOR, 'div._ac7v:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
      return driver
    # If not, it may be an user not found or error 401
    except NoSuchElementException:
      # TODO: Standardize exception handling
      raise SystemExit('User not found / Invalid session ID')

  def scrape_profile(self) -> str:
    # Based on code by https://github.com/KuanWeiBeCool/Choose-best-Sephora-Make-up-Products-With-A-Limited-Budget
    screen_height = self.driver.execute_script('return window.screen.height;')
    counter = 0

    with self.driver as driver:
      # For testing purposes, the scroll will happen at 2 times the screen hight, returning about 36 posts
      while counter <= 2:
        driver.execute_script(f'window.scrollTo(0, {screen_height * counter});')
        sleep(1)
        #scroll_height = self.driver.execute_script('return document.body.scrollHeight;')
        counter += 1

      pg_source = driver.page_source
      print('Profile scraped!')
      
    return pg_source
    

class Instuki(InstukiScraper):
  def __init__(self, username: str, session_id: str):
    InstukiScraper.__init__(self, username, session_id)
    self.soup = self.create_bs4_object()

  def create_bs4_object(self):
    page_source = self.scrape_profile()
    return BeautifulSoup(page_source, 'html.parser')

  def get_permalinks(self) -> List[str]:
    posts = self.soup.find_all('div', class_='_aabd')
    permalinks = []

    for post in posts:
      permalinks.append(f"https://www.instagram.com{post.find_all('a')[0]['href']}?__a=1&__d=dis")

    return permalinks
  
  # Currently unused, but may be useful for full-profile analysis
  def get_profile_metrics(self) -> Dict[str, int]:
    profile_metrics = {}

    for index, metric in enumerate(['total_posts', 'followers', 'following']):
      profile_metrics[metric] = self.soup.find_all('span', class_='_ac2a')[index].text

    return profile_metrics
  
  def get_post_metrics(self, post_permalink: str) -> Dict[str, int]:
    cookies = {'sessionid': self.session_id}
    try:
      response = requests.get(post_permalink, cookies=cookies)
      response.raise_for_status()
    except requests.exceptions.HTTPError as error:
      # TODO: Standardize exception handling
      raise SystemExit(error)
    
    response_json = json.loads(response.text)

    # The response format may vary, I'm not sure why
    if 'graphql' in response_json.keys():
      post_data = response_json['graphql']['shortcode_media']

      post_metrics = {
        'taken_at': post_data['taken_at_timestamp'],
        'comment_count': post_data['edge_media_preview_comment']['count'],
        'like_count': post_data['edge_media_preview_like']['count']
      }
    
    elif 'items' in response_json.keys():
      post_data = response_json['items'][0]

      post_metrics = {
        'taken_at': post_data['taken_at'],
        'comment_count': post_data['comment_count'],
        'like_count': post_data['like_count']
      }

    else:
      raise KeyError('eita')

    return post_metrics

  def get_output_dict(self) -> dict:
    output_dict = {}
    permalinks = self.get_permalinks()
    for permalink in permalinks:
      output_dict[permalink] = self.get_post_metrics(permalink)
    print('Post metrics ok!')

    return output_dict
  
  def format_to_dataframe(self) -> pd.DataFrame:
    output_dict = self.get_output_dict()

    df = (pd.DataFrame(output_dict)
            .transpose()
            .reset_index(names='permalink'))
    
    #TODO: checar o timezone, talvez alterar para UTC-3 e formatar %Y-%m-%d
    df['taken_at'] = df['taken_at'].apply(lambda x: timestamp_to_datetime(x))

    return df