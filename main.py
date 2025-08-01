from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import requests
from assets import *
import sys
import os

class Mainapp(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mainapp, self).__init__()
        uic.loadUi("WeatherApp.ui",self)
        self.setWindowTitle("WeatherApp")
        self.setWindowIcon(QIcon("assets/sun_ico.png"))
        self.setStyleSheet(open("MainStyle.qss").read())
        self.show()

        self.CityErrLabel.setVisible(False)

        self.apikey = os.environ.get('API_KEY')

        self.SearchButton.clicked.connect(self.geocode)

    # open-meteo.com/en/docs use request.get no open meteo lib
    # https://api-ninjas.com/api/geocoding


    def geocode(self):
        city = self.CityEdit.text()
        api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}'

        res = requests.get(api_url, headers={'X-Api-Key': self.apikey})

        if res.status_code == 200:
            try:
                data = res.json()[0]
                self.CityErrLabel.setVisible(False)
                print(data)
                params = {
                    'latitude': data['latitude'],
                    'longitude': data['longitude'],
                    "current": ["temperature_2m", "is_day", "weather_code"]
                }
                print(params)
                self.getWeather(params)
            except Exception as e:
                self.CityErrLabel.setVisible(True)
                print(e)
        else:
            print("Error")
            print(res.status_code)


    def getWeather(self,params : dict):
        api_url = f"https://api.open-meteo.com/v1/forecast"
        res = requests.get(api_url, params=params)
        result = res.json()
        self.setInfo(result)
        print(result)

    def setInfo(self, results:dict):
        self.CityDispLabel.setText(self.CityEdit.text())
        self.TempDispLabel.setText(str(results["current"]["temperature_2m"]) + "°C")
        self.getImage()
        self.WeatherImg.setPixmap(self.getImage())



        # img url  https://openweathermap.org/img/wn/10d@2x.png   10d == 10id d == day

    def getImage(self,url = "https://openweathermap.org/img/wn/10d@2x.png"):
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)

        return pixmap


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Mainapp()
    app.exec_()


