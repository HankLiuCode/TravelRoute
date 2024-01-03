
class Time:
    def __init__(self, hour, minute = 0):
        self.hour = hour
        self.minute = minute

    def to_minutes(self):
        return self.hour * 60 + self.minute
    
    def minute_to_hour_minute(self, minutes):
        return (minutes // 60, minutes % 60)
    
    def __str__(self) -> str:
        return f"{self.hour}:{self.minute:02}"
    
    def __sub__(self, other):
        minutes = self.to_minutes() - other.to_minutes()
        return Time(minutes // 60, minutes % 60)
    
    def __add__(self, other):
        minutes = self.to_minutes() + other.to_minutes()
        return Time(minutes // 60, minutes % 60)
    
    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute
    
    def __lt__(self, other):
        return self.to_minutes() < other.to_minutes()