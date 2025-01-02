// Function to handle destination search based on user input
function findDestination() {
    var temperature = document.getElementById('tempInput').value; // Retrieve temperature from input
    if (!temperature) {
        alert('Please enter a valid temperature.'); // Alert if no temperature is entered
        return; // Stop function execution
    }
    fetch('/getClosestWeather', { // Send request to server
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Specify JSON content type
        },
        body: JSON.stringify({temperature: temperature}) // Send temperature as JSON
    })
    .then(response => response.json()) // Parse JSON response
    .then(data => {
        handleResponse(data); // Handle data with another function
    })
    .catch(error => {
        console.error('Error:', error); // Log errors to console
        document.getElementById('destinationResult').innerHTML = 'Error fetching data.'; // Display error message
    });
}

// Function to handle the response from the server
function handleResponse(data) {
    console.log(data); // Log response data for debugging
    if (data.error) {
        document.getElementById('destinationResult').innerHTML = data.error; // Display error
        document.getElementById('moreDetailsButton').style.display = 'none'; // Hide the "More Details" button on error
    } else if (data.city && typeof data.currentTemp === 'number') {
        var display = `Closest destination with similar weather: ${data.city} (Current Temp: ${data.currentTemp}°F)`;
        document.getElementById('destinationResult').innerHTML = display; // Display weather info
        document.getElementById('moreDetailsButton').style.display = 'block'; // Show the "More Details" button

        // Add an onclick event to the "More Details" button for redirection
        document.getElementById('moreDetailsButton').onclick = function() { 
            window.location.href = `/details?city=${encodeURIComponent(data.city)}`; // Redirect to the details page with city parameter
        };
    } else {
        document.getElementById('destinationResult').innerHTML = 'No data available. Check input or try again later.';
        document.getElementById('moreDetailsButton').style.display = 'none'; // Hide the button if no data available
    }
}

