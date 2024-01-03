from typing import List
from copy import deepcopy

from .plan import Plan
from .attraction import AttractionSet, Attraction
from .distance_calculator import DistanceCalculator

class Planner:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator
    
    def generate_plans(self, attractions: List[Attraction], day_durations, start_date_str: str, end_date_str: str):
        result = []
        current_plan = Plan(self.distance_calculator, day_durations, start_date_str, end_date_str)
        visited = AttractionSet()
        days = len(day_durations)
        
        def backtrack(current_plan, day, attraction_count):
            if attraction_count == len(attractions):
                result.append(deepcopy(current_plan))
                return

            if day >= days: return

            for attraction in attractions:
                if visited.contains(attraction): continue

                if current_plan.can_append_attraction(day, attraction):
                    current_plan.append_attraction(day, attraction)
                    visited.add(attraction)

                    backtrack(current_plan, day, attraction_count+1)

                    current_plan.pop_attraction(day)
                    visited.remove(attraction)

            backtrack(current_plan, day+1, attraction_count)
        
        backtrack(current_plan, 0, 0)
        return result