from .day_plan import DayPlan
from .date import Date
from .opening_hours import OpeningHours, WeekOpeningHours
from .distance_calculator import DistanceCalculator

class Plan:
    DEFAULT_START = 8
    DEFAULT_END = 16
    
    def __init__(self, distance_calculator: DistanceCalculator, day_durations, date_start_str:str, date_end_str):
        self.date_start = Date(date_start_str)
        self.date_end = Date(date_end_str)
        
        if (self.date_end - self.date_start) + 1 != len(day_durations):
            raise Exception(f"days of duration {len(day_durations)} and dates {(self.date_end - self.date_start) + 1} must match")
        
        self.day_durations = day_durations
        self.distance_calculator = distance_calculator
        self.day_plans = [DayPlan(start, end, d, self) for d, (start, end) in enumerate(day_durations)]
        self.days = len(self.day_durations)
    
    def opening_hours(self, attraction):
        start_index = self.date_start.day_of_week_index()
        opening_hours = []
        for i in range(start_index, start_index + self.days):
            opening_hour = attraction.week_opening_hour_on(i % WeekOpeningHours.DAYS_IN_WEEK)
            opening_hours.append((opening_hour.start, opening_hour.end))
        return OpeningHours(opening_hours)

    def get(self, day):
        if day >= self.days: raise Exception("Day out of range")
        return self.day_plans[day]
    
    def can_fit_in(self, day, attraction):
        if day >= self.days: raise Exception("Day out of range")
        return self.day_plans[day].can_append_attraction(attraction)
    
    def can_append_attraction(self, day, attraction):
        if day >= self.days: raise Exception("Day out of range")
        return self.day_plans[day].can_append_attraction(attraction)

    def append_attraction(self, day, attraction):
        if day >= self.days: raise Exception("Day out of range")
        self.day_plans[day].append_attraction(attraction)

    def pop_attraction(self, day):
        if day >= self.days: raise Exception("Day out of range")
        self.day_plans[day].pop_attraction()

    def __str__(self):
        return '\n'.join([day_plan.__str__() for day_plan in self.day_plans])
    
    def to_tuple(self):
        return tuple(day_plan.to_tuple() for day_plan in self.day_plans)