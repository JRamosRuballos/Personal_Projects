# Weather App

This is a Python desktop application built with **PyQt5** that allows users to
check the current temperature (in Fahrenheit) of any city in the
**United States**. It uses the [OpenWeatherMap API](https://openweathermap.org/api) to retrieve live weather data.

The app lets users input both a **city name** and a **2-letter U.S. state code**
(e.g., `Austin`, `TX`) to fetch localized weather data. The temperature is 
converted from Kelvin to Fahrenheit, and an emoji is displayed to represent the 
current weather condition. The application also includes custom error messages 
for various issues like invalid city/state input, internet problems, or server 
errors. Styling is handled through PyQt5 stylesheets to enhance user experience.

---

## Features

- Input both **city name** and **state code**
- Converts temperature to **Fahrenheit**
- Displays a weather-related **emoji**
- Handles common API and network errors with clear messages
- Styled using **PyQt5 stylesheets** for a colorful, user-friendly interface

---

## Installation & Running

Make sure you have **Python 3** installed on your machine.

1. **Clone or download the project folder.**

2. **Install the dependencies** listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app** with:

    ```bash
    python main.py
    ```

If `python` doesn’t work, try `python3` instead depending on your system setup.

---

## Dependencies

All required packages are listed in `requirements.txt`:
- PyQt5
- requests

## Notes

- You will need an API key from 
[OpenWeatherMap](https://openweathermap.org/api). Replace the `api_key` value in
 the code with your own key.
- This project was inspired by a [YouTube tutorial](https://www.youtube.com/watch?v=Q4377DH5Jso) that originally only required city input. I expanded it to require both city and state input, added more detailed error handling, and enhanced the UI for better usability.

---

## License

This project was created for educational purposes. Feel free to use, modify, or build on it.