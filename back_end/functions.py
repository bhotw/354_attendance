
import back_end.sysConfig

def get_time():
    time.time()

    year = str(time.strftime('%Y', time.localtime(time.time())))
    month = str(time.strftime('%m', time.localtime(time.time())))
    day = str(time.strftime('d', time.localtime(time.time())))
    hour = str(time.strftime('%H',time.localtime(time.time())))
    # minute = str(time.strftime('%M',time.localtime(time.time())))
    # second = str(time.strftime('%S',time.localtime(time.time())))

    current_time = hour + '.' + minute + '.' + second + " : " + month + '.' + day + '.' + year

    return current_time
