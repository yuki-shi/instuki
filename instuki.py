from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
from utils import timestamp_to_datetime


class Instuki():
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
      raise SystemExit('User not found / Invalid session ID')

  def scrape_profile(self) -> str:
    # Based on code by https://github.com/KuanWeiBeCool/Choose-best-Sephora-Make-up-Products-With-A-Limited-Budget
    screen_height = self.driver.execute_script('return window.screen.height;')
    counter = 0

    # Logo, scrollar 2x o tamanho da tela
    while counter <= 2:
      self.driver.execute_script(f'window.scrollTo(0, {screen_height * counter});')
      sleep(1)
      #scroll_height = self.driver.execute_script('return document.body.scrollHeight;')
      counter += 1

    pg_source = self.driver.page_source
    self.driver.quit()
    
    return pg_source
  
  def get_permalinks(self) -> list:
    page_source = self.scrape_profile()
    soup = BeautifulSoup(page_source, 'html.parser')

    posts = soup.find_all('div', class_='_aabd')
    permalinks = []

    for post in posts:
      permalinks.append(f"https://www.instagram.com{post.find_all('a')[0]['href']}?__a=1&__d=dis")

    return permalinks

  def get_post_metrics(self, post_permalink: str) -> dict:
    cookies = {'sessionid': self.session_id}
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
  
  def get_output_dict(self) -> dict:
    output_dict = {}
    permalinks = self.get_permalinks()
    for permalink in permalinks:
      output_dict[permalink] = self.get_post_metrics(permalink)

    return output_dict
  
  def format_to_dataframe(self) -> pd.DataFrame:
    output_dict = self.get_output_dict()

    df = (pd.DataFrame(output_dict)
            .transpose()
            .reset_index(names='permalink'))
    
    #TODO: checar o timezone, talvez alterar para UTC-3
    df['taken_at'] = df['taken_at'].apply(lambda x: timestamp_to_datetime(x))
    return df



SESSION_ID = '146327203%3AM1Y47ijLIEg7GC%3A28%3AAYdHD8QGl38gKr_Z-yjcXSQ6yE_Om8KrioF_8zsJrw'
USERNAME = '_shimumu'

instuki = Instuki(SESSION_ID, USERNAME)
df = instuki.format_to_dataframe()
print(df.head())
df.to_csv('ig_data.csv', index=False)