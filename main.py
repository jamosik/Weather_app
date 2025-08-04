from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
import requests
from assets import *
from geoCode import *
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
        self.CityErrLabel.setVisible(False)

        self.thread = QThread()
        self.worker = GeoCode(city, self.apikey)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.handlegeocodedata)
        self.worker.error.connect(self.geocodeerror)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def handlegeocodedata(self,data):
        params = {
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            "daily": ["wind_speed_10m_max", "wind_direction_10m_dominant"],
            "current": ["temperature_2m", "is_day", "weather_code"]
        }
        self.getWeather(params)

    def geocodeerror(self,message):
        self.CityErrLabel.setVisible(False)
        self.CityErrLabel.setText(message)

    #gets weather dict from api
    def getWeather(self,params : dict):
        api_url = f"https://api.open-meteo.com/v1/forecast"
        res = requests.get(api_url, params=params)
        result = res.json()
        self.setInfo(result)
        print(result)

    #sets info in the ui
    def setInfo(self, results:dict):
        self.CityDispLabel.setText(self.CityEdit.text())
        self.TempDispLabel.setText(str(results["current"]["temperature_2m"]) + "°C")
        self.WeatherImg.setPixmap(self.getImage(self.linkprep(results)))
        for windspeediter in range(0,7):
            label = self.groupBox_Wind.findChild(QtWidgets.QLabel,f"WindSpeed{windspeediter+1}")
            if label is not None:
                label.setText(str(results["daily"]["wind_speed_10m_max"][windspeediter]))

    # preps link by getting weather code and is day
    # img url  https://openweathermap.org/img/wn/10d@2x.png   10d == 10id and  d == day

    def linkprep(self,results : dict):
        code = results["current"]["weather_code"]
        is_day = results["current"]["is_day"]
        table = {
            0: "01",
            1: "02",
            2: "03",
            3: "04",
            45: "50",
            48: "50",
            51: "09",
            61 : "10",
            71 : "13",
            95 : "11"
        }
        code = table.get(code, "01")
        time = "d" if is_day else "n"
        return f"https://openweathermap.org/img/wn/{code}{time}@2x.png"

    # gets url and creates pixmap to use
    def getImage(self,url):
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        scaledpixmap = pixmap.scaled(150,150,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        return scaledpixmap


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Mainapp()
    app.exec_()


