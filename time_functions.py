from datetime import datetime as dt
import time

def hourToBinary():
    now = dt.now()
    hour = int(now.strftime('%I'))
    first_binary = bin(hour)[2:]
    four_padded_binary_hour = first_binary.zfill(4)
    return four_padded_binary_hour

def isAM():
    # will print upcapped if in US
    now = dt.now()
    emmage = now.strftime('%p')
    if emmage == 'AM':
        return True
    if emmage == 'PM':
        return False

def getMinutes():
    now =  dt.now()
    return int(now.strftime('%M'))