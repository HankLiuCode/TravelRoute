from app.attraction import Attraction
from app.opening_hours import OpeningHours


def test_case_1():
    attraction = Attraction(0, 2, [(7, 16), (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (13, 16)])
    attraction.opening_hours('2023/12/24', '2023/12/30')
    assert attraction.opening_hours('2023/12/24', '2023/12/30').to_list() ==  [(7, 16), (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (13, 16)]
    print('test case 1 passed')

test_case_1()