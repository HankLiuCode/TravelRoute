from .visit_duration import VisitDuration

class DayPlan:
    def __init__(self, start, end, day, parent_plan):
        self.start = start
        self.end = end
        self.day = day
        self.plan = parent_plan
        self.distance_calculator = self.plan.distance_calculator
        self.visit_durations = []

    def _opening_hours(self, attraction):
        return self.plan.opening_hours(attraction)

    def _start_time(self, attraction):
        day_start = self.visit_durations[-1].end if self.visit_durations else self.start
        start_time = max(day_start, self._opening_hours(attraction).on(self.day).start)
        return start_time

    # Note that relationship between
    # - self.start self.end
    # - attraction.opening_hours
    # - travel time between attractions
    # is quite complicated
    # this version of adding travel time may be buggy
    def can_append_attraction(self, attraction):
        start_time = self._start_time(attraction)
        if self.visit_durations:
            start_time += self.distance_calculator.calculate(self.visit_durations[-1].attraction, attraction)
        
        # day related constraints
        pass_bed_time = start_time + attraction.stay_time > self.end

        # attraction related constraints
        not_enough_time = start_time + attraction.stay_time > self._opening_hours(attraction).on(self.day).end

        if pass_bed_time or not_enough_time: return False

        return True

    def append_attraction(self, attraction):
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