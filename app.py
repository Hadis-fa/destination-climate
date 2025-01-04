from flask import Flask, render_template, jsonify, request, abort
import requests

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

API_KEY = 'cf02a83079bd232e840bc5b623171abe'  # API key for weather data

# Expanded list of cities from around the world
CITIES = [
    'Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton',
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
    'Mexico City', 'Buenos Aires', 'Santiago', 'Rio de Janeiro', 'Lima',
    'London', 'Paris', 'Berlin', 'Rome', 'Madrid', 'Lisbon', 'Athens',
    'Tehran', 'Beijing', 'Tokyo', 'Seoul', 'Dubai', 'Istanbul', 'Mumbai',
    'Sydney', 'Melbourne', 'Auckland', 'Cape Town', 'Nairobi', 'Cairo',
    'Moscow', 'Warsaw', 'Prague', 'Vienna', 'Amsterdam', 'Brussels',
    'Singapore', 'Bangkok', 'Jakarta', 'Hanoi', 'Kuala Lumpur', 'Manila',
    'Riyadh', 'Doha', 'Abu Dhabi', 'Casablanca', 'Johannesburg',
    'Lagos', 'Accra', 'Algiers', 'Kinshasa', 'Dar es Salaam',
    'Ottawa', 'Quebec City', 'Halifax', 'Victoria', 'Edinburgh', 'Dublin',
    'Brisbane', 'Perth', 'Adelaide', 'Wellington', 'Christchurch',
    'Oslo', 'Stockholm', 'Copenhagen', 'Helsinki', 'Reykjavik',
    'Buenos Aires', 'Bogota', 'Quito', 'Caracas', 'Havana', 'Port-au-Prince'
]

@app.route('/')
def index():
    # Serve the main page
    return render_template('index.html')

@app.route('/getClosestWeather', methods=['POST'])
def get_closest_weather():
    # Endpoint to find the city with weather closest to the desired temperature
    data = request.get_json()  # Get data sent from the client
    desired_temp = float(data['temperature'])  # Convert temperature to float
    closest_city = None
    closest_temp = None
    smallest_diff = float('inf')  # Initialize smallest difference to infinity

    # Iterate through the list of cities and get weather data
    for city in CITIES:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial")
        if response.status_code == 200:
            city_temp = response.json().get('main', {}).get('temp')  # Extract temperature from response
            if city_temp is not None:
                temp_diff = abs(city_temp - desired_temp)
                if temp_diff < smallest_diff:
                    smallest_diff = temp_diff
                    closest_city = city
                    closest_temp = city_temp
        else:
            # Log errors if the API call fails
            print(f"Error fetching data for {city}: {response.status_code}")

    if closest_city:
        # Return the closest city and temperature if found
        return jsonify({'city': closest_city, 'currentTemp': closest_temp})
    else:
        # Return an error if no city matches
        return jsonify({'error': 'No matching city found'}), 404

@app.route('/api/weather')
def get_weather_details():
    # Endpoint to get detailed weather information
    city = request.args.get('city')
    if not city:
        # Return an error if no city parameter is provided
        return jsonify({'error': 'City parameter is missing'}), 400

    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial")
    if response.status_code == 200:
        # Parse the weather data
        data = response.json()
        weather_details = {
            'temp': data['main']['temp'],
            'weather': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'humidity': data['main']['humidity']
        }
        return jsonify(weather_details)
    else:
        # Return an error if the API call fails
        return jsonify({'error': 'Failed to fetch weather details'}), response.status_code

@app.route('/details')
def details():
    # Serve the details page with city as a parameter
    city = request.args.get('city')
    if not city:
        # If no city is provided in the query, abort with a 404 error
        abort(404)
    return render_template('details.html', city=city)

if __name__ == '__main__':
    app.run(debug=True)  # Start the application with debugging enabled

