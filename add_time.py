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
    #print(minutes)
    date = dict()

    date['days'] = minutes // 1440
    if date['days'] == 1:
        date['days_str'] = '(next day)'
    if date['days'] > 1:
        date['days_str'] = f'({date["days"]} days later)'
    #print(date.get('days', 0))

    date['hours'] = minutes % 1440 // 60 % 12 if (minutes%1440//60%12) != 0 else 12
    #print(date['hours'])

    date['part_of_the_day'] = 'PM' if (minutes%1440//60) >= 12 else 'AM'
    #print(date['part_of_the_day'])
    
    date['remaining_minutes'] = minutes%1440%60 if minutes%1440%60 > 9 else f'0{minutes%1440%60}' 
    #print(date['remaining_minutes'])

    return date


def add_time(start, duration, day_of_the_week=None):
    new_date_in_minutes = time_to_minutes(start) + time_to_minutes(duration)
    date = minutes_to_time(new_date_in_minutes)

    days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')*2
    if day_of_the_week is not None:
        days_to_go = date.get('days', 0) % 7
        date['actual_day'] = f', {days[days.index(day_of_the_week.lower()) + days_to_go].title()}'
     
    new_time =f"{date['hours']}:{date['remaining_minutes']} {date['part_of_the_day']}{date.get('actual_day','')} {date.get('days_str','')}"
    return new_time.rstrip()


start = '3:00 PM'
duration = '3:10'
print(add_time("8:16 PM", "466:02", "tuesday"))
# Returns: 6:10 PM
