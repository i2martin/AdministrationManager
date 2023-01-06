from datetime import date, timedelta


def weeknum(day_name):
    if day_name == 'Monday':
        return 0
    if day_name == 'Tuesday':
        return 1
    if day_name == 'Wednesday':
        return 2
    if day_name == 'Thursday':
        return 3
    if day_name == 'Friday':
        return 4
    if day_name == 'Saturday':
        return 5
    if day_name == 'Sunday':
        return 6


def get_workdays(year, month, days):
    for day in days:
        d = date(year, month, 1)
        d += timedelta(days=(weeknum(day) - d.weekday()) % 7)
        while d.year == year and d.month == month:
            yield d
            d += timedelta(days=7)

def order_days(workdays):
    return sorted(workdays, key=lambda x: x[:3])

