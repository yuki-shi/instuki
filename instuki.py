from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


#TODO: tornar user e session_id variáveis de ambiente
def init_driver(user: str, session_id: str) -> webdriver:
  session_id = 'xxx'
  driver = webdriver.Chrome()
  driver.get(f'https://www.instagram.com/{user}')
  driver.add_cookie({'name': 'sessionid', 'value': session_id})
  driver.get(f'https://www.instagram.com/{user}')
  return driver

driver = init_driver()
sleep(5)

# Scroll infinito
#https://github.com/KuanWeiBeCool/Choose-best-Sephora-Make-up-Products-With-A-Limited-Budget/blob/55d474f9441d0b6a1b71a44e5267b386b66b292b/Web%20Scrapping%20For%20Infinite%20Scrolling%20Websites%20Using%20Selenium.ipynb
screen_height = driver.execute_script('return window.screen.height;')
counter = 0

# Logo, scrollar 2x o tamanho da tela
while counter <= 2:
  driver.execute_script(f'window.scrollTo(0, {screen_height * counter});')
  sleep(1)
  scroll_height = driver.execute_script('return document.body.scrollHeight;')
  counter += 1

html = driver.page_source
driver.quit()

with open('pg_source.html', 'w') as f:
  f.write(html)

#post = driver.find_element(By.CSS_SELECTOR, 'div._ac7v:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
#data = driver.find_element(By.CSS_SELECTOR, 'div._ac7v:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)')
#data = data.get_attribute('alt')
#print(data)
#div._ac7v:nth-child representa as linhas
#div:nth-child vai de 1 a 3, eles representam colunas
#actions = ActionChains(driver)
#actions.move_to_element(post).perform()

#post_metrics[post.get_attribute('href')] = driver.find_element(By.CLASS_NAME, '_ac2d').text

#print(post_metrics)
