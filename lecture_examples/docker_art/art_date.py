from art import text2art
from datetime import datetime
import os


if __name__ == "__main__":
    date_format = os.environ['DATE_FORMAT']
    current_date = datetime.now().strftime(f"{date_format}")
    print(text2art(current_date, font='block'))
