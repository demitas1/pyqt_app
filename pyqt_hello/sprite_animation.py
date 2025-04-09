import sys
import warnings
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSpinBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

# 非推奨警告を抑制
warnings.filterwarnings("ignore", category=DeprecationWarning)

class ClickableLabel(QLabel):
    def __init__(self, pixmaps, parent=None):
        super().__init__(parent)
        self.pixmaps = pixmaps
        self.current_index = 0
        self.setPixmap(self.pixmaps[0])
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.animation_enabled = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_image)
        self.timer.setInterval(500)  # 500ミリ秒間隔

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.next_image()

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.pixmaps)
        self.setPixmap(self.pixmaps[self.current_index])

    def toggle_animation(self, enabled):
        self.animation_enabled = enabled
        if enabled:
            self.timer.start()
        else:
            self.timer.stop()

    def set_interval(self, interval):
        self.timer.setInterval(interval)

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
            # 方向に4枚の32x32画像を切り出し
            cropped_pixmaps = []
            for i in range(4):
                cropped = original_pixmap.copy(0, 0 + i * 32, 32, 32)
                # 2倍に拡大（nearest neighbor）
                scaled = cropped.scaled(
                    64, 64,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.FastTransformation)
                cropped_pixmaps.append(scaled)

            # クリック可能なラベルを作成
            self.image_label = ClickableLabel(cropped_pixmaps)
            layout.addWidget(self.image_label)

            # アニメーション制御用のボタンとラベル
            control_layout = QHBoxLayout()

            # 間隔設定用のスピンボックス
            interval_label = QLabel("Interval (ms):")
            self.interval_spinbox = QSpinBox()
            self.interval_spinbox.setRange(10, 2000)  # 10msから2000msまで
            self.interval_spinbox.setValue(500)  # デフォルト値
            self.interval_spinbox.setSingleStep(10)  # 10ms単位で変更
            self.interval_spinbox.valueChanged.connect(self.update_interval)
            control_layout.addWidget(interval_label)
            control_layout.addWidget(self.interval_spinbox)

            # アニメーション制御ボタン
            self.animation_button = QPushButton("animation off")
            self.animation_button.setCheckable(True)
            self.animation_button.clicked.connect(self.toggle_animation)
            control_layout.addWidget(self.animation_button)

            layout.addLayout(control_layout)
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

    def toggle_animation(self, checked):
        self.image_label.toggle_animation(checked)
        self.animation_button.setText("animation on" if checked else "animation off")

    def update_interval(self, value):
        self.image_label.set_interval(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())
