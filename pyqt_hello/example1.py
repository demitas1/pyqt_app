import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt6 Hello World')
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()
        label = QLabel('PyQt6環境のセットアップ成功！')
        layout.addWidget(label)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())
