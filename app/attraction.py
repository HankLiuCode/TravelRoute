from .opening_hours import WeekOpeningHours
from .opening_hours import OpeningHours
from .time import Time

class AttractionSet:
    def __init__(self, attractions = []):
        self.attractions = attractions
        self.attraction_ids = set([attraction.id for attraction in attractions])

    def add(self, attraction):
        if attraction.id in self.attraction_ids: return
        self.attractions.append(attraction)
        self.attraction_ids.add(attraction.id)

    def remove(self, attraction):
        self.attractions.remove(attraction)
        self.attraction_ids.remove(attraction.id)

    def contains(self, attraction):
        return attraction.id in self.attraction_ids
    
    def to_hash(self):
        " ".join([attraction_id for attraction_id in sorted(self.attraction_ids)])
    
    def __str__(self):
        return f'{self.attraction_ids}'

class Attraction:
    def __init__(self, attraction_id: int, stay_time: Time, opening_hours: list):
        self.id = attraction_id
        self.stay_time = stay_time
        self.week_opening_hours = WeekOpeningHours(opening_hours)

    def week_opening_hour_on(self, day):
        return self.week_opening_hours.on(day)
    
    def __str__(self):
        return f'{self.id}'