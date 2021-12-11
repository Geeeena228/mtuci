import datetime

def week_math(message):
    nums = int(datetime.datetime.utcnow().isocalendar()[1])
    if (nums % 2) == 0:

    elif (nums % 2) == 1:
        pass