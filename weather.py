import requests, os


api = os.environ.get('open_weather_api')
print(api)




def search_for_locations(text = "Type location: "):
    search = input(text) 
    g_link = f"http://api.openweathermap.org/geo/1.0/direct?q={search}&limit=5&appid={api}"
    r = requests.get(url=g_link)
    return list(r.json())
  

def get_coordinates():

    results = search_for_locations()
    if results == []:
        print("Can't find the location. Please try naming the location differently.")
        get_coordinates()
    else:
        for i,result in enumerate(results):
            details = ['name', 'state', 'country']
            print(f"\n{i+1}) ", end="")
            for detail in details:
                if detail in result:
                    print(f"{result[detail]};", end=" ")
        
        
        i = int(input(f"\nGive the index of your choice: "))-1
        coordinates = (int(results[i]['lat']), int(results[i]['lon']))
        return coordinates
    
def get_weather(unit="metric"):
    lat, lon = get_coordinates()

    w_link = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api}&units={unit}"
    r = requests.get(url=w_link)
    weather_data = list(dict(r.json())['list'])

    for data in weather_data:
        print(f"Time: {data['dt_txt']}, Temp: {data['main']['temp']}, Weather: {data['weather'][0]['description']}")

get_weather()