def time_to_minutes(time):
    hours = int(time.split()[0].split(':')[0])
    minutes = int(time.split()[0].split(':')[1])
    try:
        part_of_the_day = time.split()[1]
    except:
        part_of_the_day = 0

    minutes_from_midnight = 720 if part_of_the_day == 'PM' else 0
    minutes_total = hours * 60 + minutes + minutes_from_midnight

    return minutes_total



def minutes_to_time(minutes):
    print(minutes)
    date = dict()
    date['days'] = minutes // 1440
    print(date['days'])
    date['hours'] = minutes % 1440 // 60 % 12 if (minutes%1440//60%12) != 0 else 12
    print(date['hours'])
    date['part_of_the_day'] = 'PM' if date['hours'] >= 12 else 'AM'
    print(date['part_of_the_day'])
    date['remaining_minutes'] = minutes%1440%60 if minutes%1440%60 > 9 else f'0{minutes%1440%60}' 
    print(date['remaining_minutes'])
    return date


def add_time(start, duration):
    new_date_in_minutes = time_to_minutes(start) + time_to_minutes(duration)
    date = minutes_to_time(new_date_in_minutes)
    new_time =f"{date['hours']}:{date['remaining_minutes']} {date['part_of_the_day']}"
    return new_time


start = '3:00 PM'
duration = '3:10'
print(add_time("11:43 AM", "00:20"))
# Returns: 6:10 PM
