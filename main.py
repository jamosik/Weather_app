from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
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

        self.apikey = os.environ.get('API_KEY')

        self.SearchButton.clicked.connect(self.geocode)

    # open-meteo.com/en/docs use request.get no open meteo lib
    # https://api-ninjas.com/api/geocoding


    def geocode(self):
        city = self.CityEdit.text()
        api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}'
        print(api_url)
        res = requests.get(api_url, headers={'X-Api-Key': self.apikey})
        if res.status_code == 200:
            data = res.json()[0]
            print(data)
            params = {
                'latitude': data['latitude'],
                'longitude': data['longitude']
            }
            print(params)
        else:
            print("Error")

    # def getWeather(self,params):





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Mainapp()
    app.exec_()


