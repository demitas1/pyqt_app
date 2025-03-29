import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QMainWindow, QMenuBar, QMenu, QFileDialog)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_label = None
        self.scale = 2.0
        self.original_pixmap = None
        self.scale_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        self.scale_index = 1
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
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMouseTracking(True)  # マウスイベントを有効化
        layout.addWidget(self.image_label)
        main_widget.setLayout(layout)

    def wheelEvent(self, event):
        if self.original_pixmap and not self.original_pixmap.isNull():
            # ホイールの回転方向に応じてインデックスを変更
            if event.angleDelta().y() > 0:
                # 上方向の回転（ズームイン）
                self.scale_index = min(self.scale_index + 1, len(self.scale_values) - 1)
            else:
                # 下方向の回転（ズームアウト）
                self.scale_index = max(self.scale_index - 1, 0)

            # 新しいスケール値を設定して画像を更新
            self.scale = self.scale_values[self.scale_index]
            self.update_image()

    def update_image(self):
        if self.original_pixmap and not self.original_pixmap.isNull():
            # スケールを適用して画像を表示
            scaled_pixmap = self.original_pixmap.scaled(
                self.original_pixmap.size() * self.scale,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "画像ファイルを開く",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        if file_name:
            self.original_pixmap = QPixmap(file_name)
            if not self.original_pixmap.isNull():
                self.scale_index = 1  # スケールをリセット
                self.scale = self.scale_values[self.scale_index]
                self.update_image()
            else:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "エラー",
                    "画像ファイルの読み込みに失敗しました。"
                )

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
