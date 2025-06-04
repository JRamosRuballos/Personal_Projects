import sys
import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

class WeatherApp(QWidget):
    """
    Creating a weather app that takes city and state code as input.
    """
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.state_label = QLabel("Enter state code:", self)
        self.state_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        """Sets up the weather app layout"""
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.state_label)
        vbox.addWidget(self.state_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.state_label.setAlignment(Qt.AlignCenter)
        self.state_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.state_label.setObjectName("state_label")
        self.state_input.setObjectName("state_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QWidget {
                background-color: #f9ccd3;           
            }
            QLabel, QPushButton{
                font-family: Arial;
                color: #aa1945;    
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
                color: #aa1945;
            }
                           
            QLineEdit#city_input {
                font-size: 40px;
                min-height: 60px;
                color: #391306;
                background-color: #F3E5F5;
            }
            QLabel#state_label{
                font-size: 40px;
                font-style: italic;
            }
                           
            QLineEdit#state_input{
                font-size: 40px;
                min-height: 60px;
                color: #391306;
                background-color: #F3E5F5;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
                color: #4A3F55;
                background-color: #D8BFD8;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton#get_weather_button:hover {
            background-color: #E0BBE4;
            }
            QLabel#temperature_label{
                font-size: 75px;
                font-weight: bold;
            }
            QLabel#emoji_label{
                font-size: 100px;
            }
            QLabel#description_label{
                font-size: 30px;
                color: #5D3A66;
            }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        """Gets the weather using the API"""
        valid_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        }
        
        api_key = "32e02d3877e233827458cd5719818110"
        city = self.city_input.text()
        state = self.state_input.text()

        if not city or not state:
            self.display_error("Please enter both city and state code.")
            return
        if state not in valid_states:
            self.display_error("Invalid state code.\n"
                               "Enter a 2-letter U.S. state code (e.g., CA, TX)"
                               )
            return

        country = "US"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={api_key}"
        
        try:
            response = requests.get(url, timeout = 10)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key")
                case 403:
                    self.display_error("forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid Response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Time Out Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        """Displays the weather"""
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        """"Displays the weather"""
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature = data['main']['temp']
        in_fahrenheit = 1.8 * (temperature - 273.15) + 32
        weather_id = data['weather'][0]['id']
        self.temperature_label.setText(f"{in_fahrenheit:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        description = data['weather'][0]['description']
        self.description_label.setText(f"{description}")
        print(data)

    @staticmethod
    def get_weather_emoji(weather_id):
        """Returns weather emoji"""
        if weather_id >= 200 and weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌤️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return "🌤️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
