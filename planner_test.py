import unittest

from app.attraction import Attraction
from app.planner import Planner
from app.distance_calculator import DistanceCalculator
from app.time import Time
from app.utils import print_plans, print_plan

class TestPlanner(unittest.TestCase):
    
    def test_1_day_no_constraints(self):
        day_durations = [(Time(8, 0), Time(16, 0))]
        attractions = [
            Attraction(0, Time(2, 0), [(Time(8, 0), Time(16, 0)), None, None, None, None, None, None ]),
            Attraction(1, Time(2, 0), [(Time(8, 0), Time(16, 0)), None, None, None, None, None, None ]),
            Attraction(2, Time(3, 0), [(Time(8, 0), Time(16, 0)), None, None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[Time(0, 0)] * len(attractions)] * len(attractions))
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/24')
        plan0 = (((0, (Time(8, 0), Time(10, 0))), (1, (Time(10, 0), Time(12, 0))), (2, (Time(12, 0), Time(15, 0)))), )
        plan1 = (((0, (Time(8, 0), Time(10, 0))), (2, (Time(10, 0), Time(13, 0))), (1, (Time(13, 0), Time(15, 0)))), )
        plan2 = (((1, (Time(8, 0), Time(10, 0))), (0, (Time(10, 0), Time(12, 0))), (2, (Time(12, 0), Time(15, 0)))), )
        plan3 = (((1, (Time(8, 0), Time(10, 0))), (2, (Time(10, 0), Time(13, 0))), (0, (Time(13, 0), Time(15, 0)))), )
        plan4 = (((2, (Time(8, 0), Time(11, 0))), (0, (Time(11, 0), Time(13, 0))), (1, (Time(13, 0), Time(15, 0)))), )
        plan5 = (((2, (Time(8, 0), Time(11, 0))), (1, (Time(11, 0), Time(13, 0))), (0, (Time(13, 0), Time(15, 0)))), )

        self.assertEqual(generated_plans[0].to_tuple(), plan0)
        self.assertEqual(generated_plans[1].to_tuple(), plan1)
        self.assertEqual(generated_plans[2].to_tuple(), plan2)
        self.assertEqual(generated_plans[3].to_tuple(), plan3)
        self.assertEqual(generated_plans[4].to_tuple(), plan4)
        self.assertEqual(generated_plans[5].to_tuple(), plan5)

    def test_1_day_constraint(self):
        attractions = [
            Attraction(0, Time(3, 0), [(Time(8, 0), Time(11, 0)), None, None, None, None, None, None ]),
            Attraction(1, Time(2, 0), [(Time(11, 0), Time(13, 0)), None, None, None, None, None, None ]),
            Attraction(2, Time(2, 0), [(Time(14, 0), Time(16, 0)), None, None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[Time(0, 0)] * len(attractions)] * len(attractions))
        day_durations = [(Time(8, 0), Time(16, 0))]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/24')
        plan0 = (((0, (Time(8, 0), Time(11, 0))), (1, (Time(11, 0), Time(13, 0))), (2, (Time(14, 0), Time(16, 0)))), )

        self.assertEqual(generated_plans[0].to_tuple(), plan0)
    
    def test_1_day_constraint_reverse(self):
        attractions = [
            Attraction(0, Time(2, 0), [(Time(14, 0), Time(16, 0)), None, None, None, None, None, None ]),
            Attraction(1, Time(2, 0), [(Time(11, 0), Time(13, 0)), None, None, None, None, None, None ]),
            Attraction(2, Time(3, 0), [(Time(8, 0), Time(11, 0)), None, None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[Time(0, 0)] * len(attractions)] * len(attractions))
        day_durations = [(Time(8, 0), Time(16, 0))]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/24')
        plan0 = (((2, (Time(8, 0), Time(11, 0))), (1, (Time(11, 0), Time(13, 0))), (0, (Time(14, 0), Time(16, 0)))), )

        self.assertEqual(generated_plans[0].to_tuple(), plan0)

    def test_2_days(self):
        attractions = [
            Attraction(0, Time(4, 0), [None, (Time(10, 0), Time(14, 0)), None, None, None, None, None ]),
            Attraction(1, Time(3, 0), [(Time(13, 0), Time(16, 0)), None, None, None, None, None, None ]),
            Attraction(2, Time(3, 0), [(Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0)), None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[Time(0, 0)] * len(attractions)] * len(attractions))
        day_durations = [(Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0))]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/25')
        plan0 = (
            ((2, (Time(8, 0), Time(11, 0))), (1, (Time(13, 0), Time(16, 0)))), 
            ((0, (Time(10, 0), Time(14, 0))), )
        )
        self.assertEqual(generated_plans[0].to_tuple(), plan0)

    def test_3_days(self):
        attractions = [
            Attraction(0, Time(3, 0), [(Time(11, 0), Time(14, 0)), (Time(11, 0), Time(14, 0)), None, None, None, None, None]),
            Attraction(1, Time(3, 0), [None, None, (Time(13, 0), Time(16, 0)), None, None, None, None]),
            Attraction(2, Time(2, 0), [(Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0)), None, None, None, None ]),
            Attraction(3, Time(6, 0), [(Time(9, 0), Time(15, 0)), None, None, None, None, None, None])
        ]
        distance_calculator = DistanceCalculator(attractions, [[Time(0, 0)] * len(attractions)] * len(attractions))
        day_durations = [(Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0))]

        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/26')
        plan0 = (
            ((3, (Time(9, 0), Time(15, 0))), ), 
            ((0, (Time(11, 0), Time(14, 0))), (2, (Time(14, 0), Time(16, 0)))),
            ((1, (Time(13, 0), Time(16, 0))), )
        )
        plan1 = (
            ((3, (Time(9, 0), Time(15, 0))), ), 
            ((0, (Time(11, 0), Time(14, 0))), ),
            ((2, (Time(8, 0), Time(10, 0))), (1, (Time(13, 0), Time(16, 0))))
        )
        plan2 = (
            ((3, (Time(9, 0), Time(15, 0))), ), 
            ((2, (Time(8, 0), Time(10, 0))), (0, (Time(11, 0), Time(14, 0)))),
            ((1, (Time(13, 0), Time(16, 0))), )
        )
        
        self.assertEqual(generated_plans[0].to_tuple(), plan0)
        self.assertEqual(generated_plans[1].to_tuple(), plan1)
        self.assertEqual(generated_plans[2].to_tuple(), plan2)

    def test_long_running_planning(self):
        attractions = [Attraction(
            i, 
            Time(2, 0), 
            [(Time(8, 0), Time(16, 0)), 
             (Time(8, 0), Time(16, 0)), 
             (Time(8, 0), Time(16, 0)), 
             (Time(8, 0), Time(16, 0)), 
             (Time(8, 0), Time(16, 0)), 
             (Time(8, 0), Time(16, 0)), 
             (Time(8, 0), Time(16, 0)) ]) for i in range(5)]
        distance_calculator = DistanceCalculator(attractions, [[Time(0, 0)] * len(attractions)] * len(attractions))
        day_durations = [(Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0))]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/26')
        
        self.assertEqual(len(generated_plans), 2160)

    def test_1_day_with_travel_distance(self):
        attractions = [
            Attraction(0, Time(1, 0), [(Time(8, 0), Time(16, 0)), None, None, None, None, None, None ]),
            Attraction(1, Time(1, 0), [(Time(8, 0), Time(16, 0)), None, None, None, None, None, None ]),
            Attraction(2, Time(1, 0), [(Time(8, 0), Time(16, 0)), None, None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(
            attractions, 
            [[Time(0, 0), Time(10, 0), Time(10, 0)], 
             [Time(1, 0), Time(0, 0), Time(10, 0)], 
             [Time(10, 0), Time(1, 0), Time(0, 0)]])
        
        day_durations = [(Time(8, 0), Time(16, 0))]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/24')
        plan0 = (((2, (Time(8, 0), Time(9, 0))), (1, (Time(10, 0), Time(11, 0))), (0, (Time(12, 0), Time(13, 0)))), )

        self.assertEqual(generated_plans[0].to_tuple(), plan0)

    def test_3_days_across_weekend(self):
        attractions = [
            Attraction(0, Time(3, 0), [None, None, None, None, None, (Time(11, 0), Time(14, 0)), (Time(11, 0), Time(14, 0))]),
            Attraction(1, Time(3, 0), [(Time(13, 0), Time(16, 0)), None, None, None, None, None, None]),
            Attraction(2, Time(2, 0), [(Time(8, 0), Time(16, 0)), None, None, None, None, (Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0))]),
            Attraction(3, Time(6, 0), [None, None, None, None, None, (Time(9, 0), Time(15, 0)), None])
        ]
        distance_calculator = DistanceCalculator(attractions, [[Time(0, 0)] * len(attractions)] * len(attractions))
        day_durations = [(Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0)), (Time(8, 0), Time(16, 0))]

        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/29', '2023/12/31')
        plan0 = (
            ((3, (Time(9, 0), Time(15, 0))), ), 
            ((0, (Time(11, 0), Time(14, 0))), (2, (Time(14, 0), Time(16, 0)))),
            ((1, (Time(13, 0), Time(16, 0))), )
        )
        plan1 = (
            ((3, (Time(9, 0), Time(15, 0))), ), 
            ((0, (Time(11, 0), Time(14, 0))), ),
            ((2, (Time(8, 0), Time(10, 0))), (1, (Time(13, 0), Time(16, 0))))
        )
        plan2 = (
            ((3, (Time(9, 0), Time(15, 0))), ), 
            ((2, (Time(8, 0), Time(10, 0))), (0, (Time(11, 0), Time(14, 0)))),
            ((1, (Time(13, 0), Time(16, 0))), )
        )
        
        self.assertEqual(generated_plans[0].to_tuple(), plan0)
        self.assertEqual(generated_plans[1].to_tuple(), plan1)
        self.assertEqual(generated_plans[2].to_tuple(), plan2)
    

if __name__ == '__main__':
    unittest.main()