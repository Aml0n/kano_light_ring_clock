from datetime import datetime as dt
import time

def hour_to_binary():
    now = dt.now()
    hour = int(now.strftime('%I'))
    first_binary = bin(hour)[2:]
    four_padded_binary_hour = first_binary.zfill(4)
    return four_padded_binary_hour

def am_or_pm():
    # will print upcapped if in US
    now = dt.now()
    return now.strftime('%p')

def get_minutes():
    now =  dt.now()
    return int(now.strftime('%M'))
# hour_to_binary()
# am_or_pm()