from typing import List
from .date import Date
from .opening_hours import OpeningHours, WeekOpeningHours
from .distance_calculator import DistanceCalculator
from .visit_duration import VisitDuration
from .attraction import Attraction
from .time import Time

class Plan:
    DEFAULT_START = 8
    DEFAULT_END = 16
    
    def __init__(self, distance_calculator: DistanceCalculator, day_durations: List[tuple], date_start_str: str, date_end_str: str):
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

class DayPlan:
    def __init__(self, start: Time, end: Time, day: int, parent_plan: Plan):
        self.start = start
        self.end = end
        self.day = day
        self.plan = parent_plan
        self.distance_calculator = self.plan.distance_calculator
        self.visit_durations = []

    def _opening_hours(self, attraction: Attraction):
        return self.plan.opening_hours(attraction)

    def _start_time(self, attraction: Attraction):
        day_start = self.visit_durations[-1].end if self.visit_durations else self.start
        start_time = max(day_start, self._opening_hours(attraction).on(self.day).start)
        return start_time

    # Note that relationship between
    # - self.start self.end
    # - attraction.opening_hours
    # - travel time between attractions
    # is quite complicated
    # this version of adding travel time may be buggy
    def can_append_attraction(self, attraction: Attraction):
        start_time = self._start_time(attraction)
        if self.visit_durations:
            start_time += self.distance_calculator.calculate(self.visit_durations[-1].attraction, attraction)
        
        # day related constraints
        pass_bed_time = start_time + attraction.stay_time > self.end

        # attraction related constraints
        not_enough_time = start_time + attraction.stay_time > self._opening_hours(attraction).on(self.day).end

        if pass_bed_time or not_enough_time: return False

        return True

    def append_attraction(self, attraction: Attraction):
        start_time = self._start_time(attraction)
        if self.visit_durations:
            start_time += self.distance_calculator.calculate(self.visit_durations[-1].attraction, attraction)
        visit_duration = VisitDuration(start_time, attraction)
        self.visit_durations.append(visit_duration)

    def pop_attraction(self):
        self.visit_durations.pop()
    
    def __str__(self):
        attraction_strs = [visit_duration.__str__() for visit_duration in self.visit_durations]
        return f'Day {self.day}: {attraction_strs}'
    
    def to_tuple(self):
        return tuple(visit_duration.to_tuple() for visit_duration in self.visit_durations)