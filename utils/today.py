import datetime

def get_date():
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    return "Hello, today is " + str(formatted_date)
