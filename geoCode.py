from PyQt5.QtCore import Qt, QThread,QObject, pyqtSignal
import requests
from PyQt5 import QtWidgets, uic

class GeoCode(QObject):


    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, city,apiKey):
        super().__init__()
        self.city = city
        self.apiKey = apiKey


    def run(self):
        api_url = f'https://api.api-ninjas.com/v1/geocoding?city={self.city}'

        res = requests.get(api_url, headers={'X-Api-Key': self.apiKey})

        if res.status_code == 200:
            try:
                data = res.json()[0]
                print(data)
                self.finished.emit(data)
            except Exception as e:
                self.error.emit(f"Api Error: {res.status_code}")
                print(e)
        else:
            print("Error")
            print(res.status_code)