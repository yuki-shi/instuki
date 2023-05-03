from instuki import Instuki
import pandas as pd
from time import sleep

SESSION_ID = 'xxx'

if __name__ == '__main__':

  dfs = []
  usernames = ['_shimumu', '_funeralha']

  for username in usernames:
    print(f"Getting {username}'s data...")

    instuki = Instuki(SESSION_ID, username)
    df = instuki.format_to_dataframe()
    df['account'] = username

    print(df.head())
    
    dfs.append(df)

    # Better safe than sorry?
    sleep(10)


  df_final = pd.concat(dfs)
  df_final.to_csv('ig_data.csv', index=False)
