import requests
import sys
from geocoder_find_map_params import get_map_params

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow


class MapSearcher(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.searchButton.clicked.connect(self.run)
        self.checkBox.stateChanged.connect(self.getImage)
        self.delta = 1
        self.delta_ll = 0.5


    def run(self):
        self.getImage()


    def getImage(self):
        api_server = "https://static-maps.yandex.ru/v1"
        lon = self.lon.text()
        lat = self.lat.text()
        delta1 = str(float(self.spn.text()))
        delta2 = str(float(self.spn.text()))
        apikey = "e2a0aacc-0eb4-49b9-93c9-4caa526805a3"
        self.toponym_to_find = self.toponym.text()
        print(self.toponym_to_find)

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta1, delta2]),
            'theme': 'dark' if self.checkBox.isChecked() else 'light',
            "apikey": apikey,
        }
        response = requests.get(api_server, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            exit()

        if event.key() == Qt.Key.Key_PageUp:
            val = float(self.spn.text())
            res = val + self.delta
            res = min(79, round(res, 2))
            self.spn.setText(str(res))
            self.getImage()

        if event.key() == Qt.Key.Key_PageDown:
            val = float(self.spn.text())
            res = val - self.delta
            res = max(0.001, round(res, 2))
            self.spn.setText(str(res))
            self.getImage()

        if event.key() == Qt.Key.Key_Down:
            val_lat = float(self.lat.text())
            val_lat -= self.delta_ll * float(self.spn.text())
            self.lat.setText(str(val_lat))
            self.getImage()

        if event.key() == Qt.Key.Key_Up:
            val_lat = float(self.lat.text())
            val_lat += self.delta_ll * float(self.spn.text())
            self.lat.setText(str(val_lat))
            self.getImage()

        if event.key() == Qt.Key.Key_Left:
            val_lon = float(self.lon.text())
            val_lon -= self.delta_ll * float(self.spn.text())
            self.lon.setText(str(val_lon))
            self.getImage()

        if event.key() == Qt.Key.Key_Right:
            val_lon = float(self.lon.text())
            val_lon += self.delta_ll * float(self.spn.text())
            self.lon.setText(str(val_lon))
            self.getImage()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapSearcher()
    ex.show()
    sys.exit(app.exec())