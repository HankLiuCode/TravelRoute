import unittest

from app.attraction import Attraction
from app.planner import Planner
from app.distance_calculator import DistanceCalculator
from app.utils import print_plans, print_plan

class TestPlanner(unittest.TestCase):
    
    def test_1_day_no_constraints(self):
        day_durations = [(8, 16)]
        attractions = [
            Attraction(0, 2, [(8, 16), None, None, None, None, None, None ]),
            Attraction(1, 2, [(8, 16), None, None, None, None, None, None ]),
            Attraction(2, 3, [(8, 16), None, None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[0] * len(attractions)] * len(attractions))
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/24')
        plan0 = (((0, (8, 10)), (1, (10, 12)), (2, (12, 15))), )
        plan1 = (((0, (8, 10)), (2, (10, 13)), (1, (13, 15))), )
        plan2 = (((1, (8, 10)), (0, (10, 12)), (2, (12, 15))), )
        plan3 = (((1, (8, 10)), (2, (10, 13)), (0, (13, 15))), )
        plan4 = (((2, (8, 11)), (0, (11, 13)), (1, (13, 15))), )
        plan5 = (((2, (8, 11)), (1, (11, 13)), (0, (13, 15))), )

        self.assertEqual(generated_plans[0].to_tuple(), plan0)
        self.assertEqual(generated_plans[1].to_tuple(), plan1)
        self.assertEqual(generated_plans[2].to_tuple(), plan2)
        self.assertEqual(generated_plans[3].to_tuple(), plan3)
        self.assertEqual(generated_plans[4].to_tuple(), plan4)
        self.assertEqual(generated_plans[5].to_tuple(), plan5)

    def test_1_day_constraint(self):
        attractions = [
            Attraction(0, 3, [(8, 11), None, None, None, None, None, None ]),
            Attraction(1, 2, [(11, 13), None, None, None, None, None, None ]),
            Attraction(2, 2, [(14, 16), None, None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[0] * len(attractions)] * len(attractions))
        day_durations = [(8, 16)]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/24')
        plan0 = (((0, (8, 11)), (1, (11, 13)), (2, (14, 16))), )

        self.assertEqual(generated_plans[0].to_tuple(), plan0)
    
    def test_1_day_constraint_reverse(self):
        attractions = [
            Attraction(0, 2, [(14, 16), None, None, None, None, None, None ]),
            Attraction(1, 2, [(11, 13), None, None, None, None, None, None ]),
            Attraction(2, 3, [(8, 11), None, None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[0] * len(attractions)] * len(attractions))
        day_durations = [(8, 16)]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/24')
        plan0 = (((2, (8, 11)), (1, (11, 13)), (0, (14, 16))), )

        self.assertEqual(generated_plans[0].to_tuple(), plan0)

    def test_2_days(self):
        attractions = [
            Attraction(0, 4, [None, (10, 14), None, None, None, None, None ]),
            Attraction(1, 3, [(13, 16), None, None, None, None, None, None ]),
            Attraction(2, 3, [(8, 16), (8, 16), None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[0] * len(attractions)] * len(attractions))
        day_durations = [(8, 16), (8, 16)]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/25')
        plan0 = (
            ((2, (8, 11)), (1, (13, 16))), 
            ((0, (10, 14)), )
        )
        self.assertEqual(generated_plans[0].to_tuple(), plan0)

    def test_3_days(self):
        attractions = [
            Attraction(0, 3, [(11, 14), (11, 14), None, None, None, None, None]),
            Attraction(1, 3, [None, None, (13, 16), None, None, None, None]),
            Attraction(2, 2, [(8, 16), (8, 16), (8, 16), None, None, None, None ]),
            Attraction(3, 6, [(9, 15), None, None, None, None, None, None])
        ]
        distance_calculator = DistanceCalculator(attractions, [[0] * len(attractions)] * len(attractions))
        day_durations = [(8, 16), (8, 16), (8, 16)]

        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/26')
        plan0 = (
            ((3, (9, 15)), ), 
            ((0, (11, 14)), (2, (14, 16))),
            ((1, (13, 16)), )
        )
        plan1 = (
            ((3, (9, 15)), ), 
            ((0, (11, 14)), ),
            ((2, (8, 10)), (1, (13, 16)))
        )
        plan2 = (
            ((3, (9, 15)), ), 
            ((2, (8, 10)), (0, (11, 14))),
            ((1, (13, 16)), )
        )
        
        self.assertEqual(generated_plans[0].to_tuple(), plan0)
        self.assertEqual(generated_plans[1].to_tuple(), plan1)
        self.assertEqual(generated_plans[2].to_tuple(), plan2)

    def test_long_running_planning(self):
        attractions = [Attraction(i, 2, [(8, 16), (8, 16), (8, 16), (8, 16), (8, 16), (8, 16), (8, 16) ]) for i in range(5)]
        distance_calculator = DistanceCalculator(attractions, [[0] * len(attractions)] * len(attractions))
        day_durations = [(8, 16), (8, 16), (8, 16)]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/26')
        
        self.assertEqual(len(generated_plans), 2160)

    def test_1_day_with_travel_distance(self):
        attractions = [
            Attraction(0, 1, [(8, 16), None, None, None, None, None, None ]),
            Attraction(1, 1, [(8, 16), None, None, None, None, None, None ]),
            Attraction(2, 1, [(8, 16), None, None, None, None, None, None ])
        ]
        distance_calculator = DistanceCalculator(attractions, [[0, 10, 10], [1, 0, 10], [10, 1, 0]])
        day_durations = [(8, 16)]
        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/24', '2023/12/24')
        plan0 = (((2, (8, 9)), (1, (10, 11)), (0, (12, 13))), )

        self.assertEqual(generated_plans[0].to_tuple(), plan0)

    def test_3_days_across_weekend(self):
        attractions = [
            Attraction(0, 3, [None, None, None, None, None, (11, 14), (11, 14)]),
            Attraction(1, 3, [(13, 16), None, None, None, None, None, None]),
            Attraction(2, 2, [(8, 16), None, None, None, None, (8, 16), (8, 16)]),
            Attraction(3, 6, [None, None, None, None, None, (9, 15), None])
        ]
        distance_calculator = DistanceCalculator(attractions, [[0] * len(attractions)] * len(attractions))
        day_durations = [(8, 16), (8, 16), (8, 16)]

        generated_plans = Planner(distance_calculator).generate_plans(attractions, day_durations, '2023/12/29', '2023/12/31')
        plan0 = (
            ((3, (9, 15)), ), 
            ((0, (11, 14)), (2, (14, 16))),
            ((1, (13, 16)), )
        )
        plan1 = (
            ((3, (9, 15)), ), 
            ((0, (11, 14)), ),
            ((2, (8, 10)), (1, (13, 16)))
        )
        plan2 = (
            ((3, (9, 15)), ), 
            ((2, (8, 10)), (0, (11, 14))),
            ((1, (13, 16)), )
        )
        
        self.assertEqual(generated_plans[0].to_tuple(), plan0)
        self.assertEqual(generated_plans[1].to_tuple(), plan1)
        self.assertEqual(generated_plans[2].to_tuple(), plan2)
    

if __name__ == '__main__':
    unittest.main()