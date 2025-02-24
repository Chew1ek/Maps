import sys, requests

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow


class MapSearcher(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.searchButton.clicked.connect(self.run)
        self.delta = 1

    def run(self):
        self.getImage()


    def getImage(self):
        api_server = "https://static-maps.yandex.ru/v1"
        lon = self.lon.text()
        lat = self.lat.text()
        delta1 = str(float(self.spn.text()) + float(self.delta))
        delta2 = str(float(self.spn.text()) + float(self.delta))
        apikey = "e2a0aacc-0eb4-49b9-93c9-4caa526805a3"

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta1, delta2]),
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapSearcher()
    ex.show()
    sys.exit(app.exec())