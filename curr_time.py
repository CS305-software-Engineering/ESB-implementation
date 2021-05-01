import time
import datetime


def get_curr_time():
    """return current timestamp in MYSQL format"""
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(
        '%Y-%m-%d %H:%M:%S')
    return timestamp
