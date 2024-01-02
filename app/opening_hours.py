class OpeningHour:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class OpeningHours:
    NotOpen = OpeningHour(25, -1)
    
    def __init__(self, opening_hours):
        self.opening_hours = [OpeningHour(oh[0], oh[1]) if oh != None else OpeningHours.NotOpen for oh in opening_hours]
    
    def on(self, day):
        if day >= len(self.opening_hours) or day < 0: raise Exception("Day out of range")
        return self.opening_hours[day]
    
    def to_list(self):
        return [(oh.start, oh.end) for oh in self.opening_hours]

class WeekOpeningHours:
    DAYS_IN_WEEK = 7
    NotOpen = OpeningHour(25, -1)
    
    def __init__(self, opening_hours):
        if len(opening_hours) != WeekOpeningHours.DAYS_IN_WEEK:
            raise Exception("Invalid opening hours")
        self.opening_hours = [OpeningHour(oh[0], oh[1]) if oh != None else WeekOpeningHours.NotOpen for oh in opening_hours]
    
    def on(self, day):
        if day >= WeekOpeningHours.DAYS_IN_WEEK or day < 0: raise Exception("Day out of range")
        return self.opening_hours[day]
    
    def to_list(self):
        return [(oh.start, oh.end) for oh in self.opening_hours]