import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel, QSlider, QPushButton
from PyQt6.QtGui import QPixmap, QAction, QResizeEvent
from PyQt6.QtCore import Qt
from PyQt6 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Qt Designerで作成したUIファイルを読み込む
        uic.loadUi("mainwindow.ui", self)

        # ウィジェットへの参照を取得
        # ※注意: objectNameがQt Designerで設定した名前と一致している必要があります
        self.imageLabel = self.findChild(QLabel, "imageLabel")
        self.slider1 = self.findChild(QSlider, "slider1")
        self.slider2 = self.findChild(QSlider, "slider2")
        self.button1 = self.findChild(QPushButton, "button1")
        self.button2 = self.findChild(QPushButton, "button2")

        # シグナル/スロットの接続
        self.slider1.valueChanged.connect(self.slider1_changed)
        self.slider2.valueChanged.connect(self.slider2_changed)
        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)

        # メニューアクションの接続
        # ※注意: objectNameがQt Designerで設定した名前と一致している必要があります
        self.actionOpen_Image = self.findChild(QAction, "actionOpenImage")
        self.actionExit = self.findChild(QAction, "actionExit")
        self.actionAbout_App = self.findChild(QAction, "actionAboutApp")

        self.actionOpen_Image.triggered.connect(self.open_image)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout_App.triggered.connect(self.show_about)

        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setMinimumSize(100, 100)  # 最小サイズを設定
        self.current_pixmap = None

    def resizeEvent(self, event: QResizeEvent):
        """ウィンドウサイズ変更時に画像をリサイズする"""
        super().resizeEvent(event)

        # 画像が読み込まれている場合は再スケーリング
        if self.current_pixmap:
            self.scale_image()

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "画像を開く", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_name:
            self.current_pixmap = QPixmap(file_name)

            if not self.current_pixmap.isNull():
                # 画像を適切なサイズにスケーリングして表示
                self.scale_image()
                print(f"画像を開きました: {file_name}")
            else:
                print("画像の読み込みに失敗しました")

    def scale_image(self):
        """現在のラベルサイズに合わせて画像をスケーリング"""
        if not self.current_pixmap or self.current_pixmap.isNull():
            return

        # ラベルのサイズを取得
        label_size = self.imageLabel.size()

        # アスペクト比を維持しながら画像をスケーリング
        scaled_pixmap = self.current_pixmap.scaled(
            label_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # スケーリングされた画像を表示
        self.imageLabel.setPixmap(scaled_pixmap)

    def show_about(self):
        QMessageBox.about(
            self,
            "About Application",
            "PyQt6 GUIアプリケーションのサンプルです。"
        )
        print("Aboutダイアログを表示しました")

    def slider1_changed(self, value):
        print(f"スライダー1の値が変更されました: {value}")

    def slider2_changed(self, value):
        print(f"スライダー2の値が変更されました: {value}")

    def button1_clicked(self):
        print("ボタン1がクリックされました")

    def button2_clicked(self):
        print("ボタン2がクリックされました")

# アプリケーションの実行
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
