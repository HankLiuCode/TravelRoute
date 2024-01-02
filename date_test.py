from app.date import Date

def test_case_1():
    test_dates = [
        '2023/12/24',
        '2023/12/25',
        '2023/12/26',
        '2023/12/27',
        '2023/12/28',
        '2023/12/29',
        '2023/12/30',
    ]
    correct = [
        ('Sunday', 0),
        ('Monday', 1),
        ('Tuesday', 2),
        ('Wednesday', 3),
        ('Thursday', 4),
        ('Friday', 5),
        ('Saturday', 6),
    ]
    for t, c in zip(test_dates, correct):
        date = Date(t)
        assert date.day_of_week() == c[0]
        assert date.day_of_week_index() == c[1]
    print('test case 1 passed')

test_case_1()