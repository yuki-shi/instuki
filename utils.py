import datetime as dt

def timestamp_to_datetime(timestamp:int) -> dt.datetime:
  return dt.datetime.utcfromtimestamp(timestamp)