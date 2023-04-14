
import sysConfig as se
# import time

def get_time():
    se.time.time()

    # year = str(se.time.strftime('%Y', se.time.localtime(se.time.time())))
    # month = str(se.time.strftime('%m', time.localtime(time.time())))
    # day = str(time.strftime('d', time.localtime(time.time())))
    # hour = str(time.strftime('%H', time.localtime(time.time())))
    # minute = str(time.strftime('%M', time.localtime(time.time())))
    # second = str(time.strftime('%S', time.localtime(time.time())))
    #
    # current_time = hour + '.' + minute + '.' + second + " : " + month + '.' + day + '.' + year
    current_time = se.time.localtime(se.time.time)

    return current_time
