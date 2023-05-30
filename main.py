from instuki import Instuki
import pandas as pd
import os
import sys
from time import sleep
import argparse

if __name__ == '__main__':

 # From the keyword argument, create a list of usernames to be scraped
  parser = argparse.ArgumentParser()
  parser.add_argument('-u',
                      '--username',
                      help='Instagram usernames in list input',
                      type=str)
  args = parser.parse_args()
  
  try:
    usernames = [x for x in args.username.split(',')]
  except AttributeError:
    sys.exit('Correct usage "python3 main.py -u {USERNAME_LIST}"')

  # Getting session id from the environmental variables
  if 'SESSION_ID' in os.environ: 
    SESSION_ID = os.getenv('SESSION_ID')
  else:
    sys.exit('No SESSION_ID found in environmental variables.\nUse: export SESSION_ID={session_id}')

  # Run the process for each username inputted
  dfs = []
  
  for username in usernames:
    print(f"Getting {username}'s data...")

    instuki = Instuki(SESSION_ID, username)
    df = instuki.format_to_dataframe()
    df['account'] = username

    print(f'Got {df.shape[0]} posts!')
    
    dfs.append(df)

    # Better safe than sorry?
    sleep(10)

  # Concat all results into an aggregated dataframe, then export to csv format
  df_final = pd.concat(dfs)
  df_final.to_csv('ig_data.csv', index=False)
  print('Data saved to ./ig_data.csv')
