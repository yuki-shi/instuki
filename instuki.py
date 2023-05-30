from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import sys
from utils import timestamp_to_datetime


class InstukiScraper():
  def __init__(self, session_id: str, username: str):
    """
    Initializes the scraper class.

    Args:
    session_id (str): Cookie got from an logged in Instagram account 
    username (str): Username of the account to be scraped

    Returns:
    None
    """
    self.session_id = session_id
    self.username = username
    self.driver = self.init_driver()

  def init_driver(self) -> webdriver:
    """
    Initializes the webdriver with the specified options

    Args:
    None

    Returns:
    webdriver.Chrome: The initialized webdriver
     """
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
      sys.exit('User not found / Invalid session ID')

  def scrape_profile(self) -> str:
    """
    Scrape the profile of inputted username.
    Since Instagram has an infinite scroll, the page will be scrolled thrice, returning about 30 posts.

    Args:
    None

    Returns:
    str: Scraped page source.

    Based on code by https://github.com/KuanWeiBeCool/Choose-best-Sephora-Make-up-Products-With-A-Limited-Budget
    """
    screen_height = self.driver.execute_script('return window.screen.height;')
    counter = 0

    with self.driver as driver:
      while counter <= 3:
        driver.execute_script(f'window.scrollTo(0, {screen_height * counter});')
        #scroll_height = self.driver.execute_script('return document.body.scrollHeight;')
        counter += 1
        sleep(3)

      pg_source = driver.page_source
      print('Profile scraped!')
      
    return pg_source
    

class Instuki(InstukiScraper):
  def __init__(self, username: str, session_id: str):
    """
    Initializes the main transformation class by inheriting InstukiScraper.
    """
    InstukiScraper.__init__(self, username, session_id)
    self.soup = self.create_bs4_object()

  def create_bs4_object(self) -> BeautifulSoup:
    """
    From the scraped page source, instanciate a beautiful soup object.

    Args:
    None

    Returns:
    BeautifulSoup: Instanciated beautiful soup object.
    """
    page_source = self.scrape_profile()
    return BeautifulSoup(page_source, 'html.parser')

  def get_permalinks(self) -> List[str]:
    """
    Find all posts' permalinks

    Args:
    None
    
    Returns:
    List[str]: List containing each post permalink from the scraped profile
    """
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
    """
    Get public metrics (created date, likes and comments) for a given post.

    Args:
    post_permalink (str): Permalink of an Instagram post.

    Returns:
    Dict[str, int]: Dictionary containing each post metric name as key and metric value as value.
    """
    cookies = {'sessionid': self.session_id}
    try:
      response = requests.get(post_permalink, cookies=cookies)
      response.raise_for_status()
    except requests.exceptions.HTTPError as error:
      sys.exit(error)
    
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
    """
    Aggregate all post metric result dictionaries into one.

    Args:
    None

    Returns:
    dict: dictionary of dictionaries with all the posts scraped and their metrics. 
    """
    output_dict = {}
    permalinks = self.get_permalinks()
    for permalink in permalinks:
      output_dict[permalink] = self.get_post_metrics(permalink)
    print('Post metrics ok!')

    return output_dict
  
  def format_to_dataframe(self) -> pd.DataFrame:
    """
    Format a dictionary of dictionaries into a dataframe and perform basic data transformation.

    Args:
    None

    Returns:
    pd.DataFrame: Inputted dictionary in dataframe format. 
    """
    output_dict = self.get_output_dict()

    df = (pd.DataFrame(output_dict)
            .transpose()
            .reset_index(names='permalink'))
    
    # Format timestamp into datetime
    #TODO: checar o timezone, talvez alterar para UTC-3 e formatar %Y-%m-%d
    df['taken_at'] = df['taken_at'].apply(lambda x: timestamp_to_datetime(x))
    
    # Format the URL back to an user-friendly version
    df['permalink'] = df['permalink'].str.replace(r'(?=\?).*', '', regex=True)
    return df
