import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt6 Hello World')
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        # PNGファイルを読み込んで処理
        original_pixmap = QPixmap("image.png")  # 画像ファイルのパスを指定してください
        if not original_pixmap.isNull():
            # 左上から32x32の領域を切り出し
            cropped_pixmap = original_pixmap.copy(0, 0, 32, 32)
            # 2倍に拡大（nearest neighbor）
            scaled_pixmap = cropped_pixmap.scaled(
                64, 64,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation)

            image_label = QLabel()
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(image_label)
        else:
            # 画像の読み込みに失敗した場合のエラーメッセージ
            error_label = QLabel('画像の読み込みに失敗しました')
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label)

        # テキストラベル
        text_label = QLabel('PyQt6環境のセットアップ成功！')
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())
