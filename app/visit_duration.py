from .time import Time
from .attraction import Attraction

class VisitDuration:
    def __init__(self, start: Time, attraction: Attraction):
        self.start = start
        self.end = start + attraction.stay_time
        self.attraction = attraction
    def __str__(self):
        return f'{self.attraction.__str__()} ({self.start}, {self.end})'
    
    def to_tuple(self):
        return (self.attraction.id, (self.start, self.end))