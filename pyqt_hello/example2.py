import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QMainWindow, QMenuBar, QMenu, QFileDialog)
from PyQt6.QtCore import Qt

class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt6 Hello World')
        self.setGeometry(100, 100, 800, 600)

        # メインメニューの作成
        menubar = self.menuBar()

        # File メニュー
        file_menu = menubar.addMenu('File')

        # Open アクション
        open_action = file_menu.addAction('Open')
        open_action.triggered.connect(self.open_file)

        # セパレータ
        file_menu.addSeparator()

        # Exit アクション
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)

        # About メニュー
        about_menu = menubar.addMenu('About')
        about_action = about_menu.addAction('About')
        about_action.triggered.connect(self.show_about)

        # メインウィジェットの設定
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # レイアウトの設定
        layout = QVBoxLayout()
        label = QLabel('PyQt6環境のセットアップ成功！')
        layout.addWidget(label)
        main_widget.setLayout(layout)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "ファイルを開く",
            "",
            "All Files (*);;Text Files (*.txt);;Python Files (*.py)"
        )
        if file_name:
            print(f"選択されたファイル: {file_name}")

    def show_about(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About",
            "PyQt6 Hello World\n\n"
            "シンプルなPyQt6アプリケーションの例です。"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())
