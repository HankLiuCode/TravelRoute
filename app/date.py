from datetime import datetime

class Date:
    DAY_MAPPING = {
        "Sunday": 0,
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6
    }
    def __init__(self, date_string: str):
        self.date_string = date_string

    def day_of_week(self):
        date = datetime.strptime(self.date_string, "%Y/%m/%d")
        day_of_week = date.strftime("%A")
        return day_of_week
    
    def day_of_week_index(self):
        day = self.day_of_week()
        return Date.DAY_MAPPING[day]
    
    def __sub__(self, other):
        date = datetime.strptime(self.date_string, "%Y/%m/%d")
        other_date = datetime.strptime(other.date_string, "%Y/%m/%d")
        return (date - other_date).days