// Wait for the entire content of the webpage to load before executing the code
document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the city query parameter from the URL
    const params = new URLSearchParams(window.location.search);
    const city = params.get('city');

    // Fetch weather details if city is specified, else show an error message
    if (city) {
        fetchWeatherDetails(city);
    } else {
        document.getElementById('weather-info').textContent = 'City not specified';
    }
});

// Function to fetch weather details from the server
function fetchWeatherDetails(city) {
    fetch(`/api/weather?city=${encodeURIComponent(city)}`)
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            document.getElementById('weather-info').textContent = 'Error fetching data';
            console.error('Error:', data.error);
        } else {
            updateWeatherDetails(data, city);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        document.getElementById('weather-info').textContent = 'Failed to load data';
    });
}

// Function to update the DOM with the fetched weather details
function updateWeatherDetails(data, city) {
    document.getElementById('cityName').textContent = city;
    document.getElementById('temperature').textContent = `Temperature: ${data.temp}°C`;
    document.getElementById('weather').textContent = `Weather: ${data.weather}`;
    document.getElementById('humidity').textContent = `Humidity: ${data.humidity}%`;
    document.getElementById('wind').textContent = `Wind: ${data.wind_speed} km/h`;
    document.getElementById('more-info').textContent = `More details about the weather conditions in ${city}.`;
}
