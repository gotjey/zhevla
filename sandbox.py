weather_data = [{'city': 'New York', 'temperature': 6.79, 'description': 'broken clouds', 'icon': '04d'}, {'city': 'London', 'temperature': 11.64, 'description': 'overcast clouds', 'icon': '04d'}, {'city': 'Tokyo', 'temperature': 6.33, 'description': 'broken clouds', 'icon': '04n'}]


for i in weather_data:
    print(i['city'])
    print(i['temperature'])