from datetime import datetime
from art import text2art


def todays_date_in_str_art():
    date_str = datetime.now().strftime('%m/%Y')
    ascii_art_date = text2art(date_str, font='block')
    return ascii_art_date


if __name__ == "__main__":
    print(todays_date_in_str_art())