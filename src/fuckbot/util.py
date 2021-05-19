def pp_time(time_seconds):
    # it's pp time
    hours = time_seconds // 3600
    time_seconds %= 3600

    minutes = time_seconds // 60
    time_seconds %= 60

    return "{}h:{}m:{}s".format(hours, minutes, time_seconds)
