from instuki import Instuki

SESSION_ID = '146327203%3AM1Y47ijLIEg7GC%3A28%3AAYdHD8QGl38gKr_Z-yjcXSQ6yE_Om8KrioF_8zsJrw'
USERNAME = '_shimumu'

if __name__ == '__main__':
  instuki = Instuki(SESSION_ID, USERNAME)
  df = instuki.format_to_dataframe()
  print(df.head())
  df.to_csv('ig_data.csv', index=False)
