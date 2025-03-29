import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QMainWindow, QMenuBar, QMenu, QFileDialog)
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QRect, QPoint

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = None
        self.scale = 1.0

    def setScale(self, scale):
        self.scale = scale
        self.update()  # スケール変更時に再描画

    def setPixmap(self, pixmap):
        self.original_pixmap = pixmap
        super().setPixmap(pixmap)

class SelectionRect(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawing = False
        self.rect_start = QPoint()
        self.rect_end = QPoint()
        self.current_rect = None  # スケール1.0での矩形
        self.scaled_rect = None   # 現在のスケールでの矩形
        self.scale = 1.0
        # 背景を透明に設定
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def setScale(self, scale):
        self.scale = scale
        # scaled_rectを更新
        if self.current_rect is not None:
            self.scaled_rect = QRect(
                int(self.current_rect.x() * scale),
                int(self.current_rect.y() * scale),
                int(self.current_rect.width() * scale),
                int(self.current_rect.height() * scale)
            )
            print(f"scale: {scale}")
            print(f"current_rect: {self.current_rect.x()}, {self.current_rect.y()}, {self.current_rect.width()}, {self.current_rect.height()}")
            print(f"scaled_rect: {self.scaled_rect.x()}, {self.scaled_rect.y()}, {self.scaled_rect.width()}, {self.scaled_rect.height()}")
        self.update()  # スケール変更時に再描画

    def paintEvent(self, event):
        if self.drawing or self.scaled_rect is not None:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(0, 0, 255), 2))  # 青い線、太さ2
            if self.drawing:
                painter.drawRect(self.get_rect())
            else:
                painter.drawRect(self.scaled_rect)

    def get_rect(self):
        return QRect(self.rect_start, self.rect_end).normalized()

    def scale_rect_to_original(self, rect):
        if self.scale == 0:
            return rect
        return QRect(
            int(rect.x() / self.scale),
            int(rect.y() / self.scale),
            int(rect.width() / self.scale),
            int(rect.height() / self.scale)
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.current_rect is not None:
                # 既存の矩形を消去
                self.current_rect = None
                self.scaled_rect = None
                self.update()
            # 新しい矩形の開始
            self.drawing = True
            self.rect_start = event.pos()
            self.rect_end = self.rect_start

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.rect_end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            self.rect_end = event.pos()
            # 矩形の座標を標準出力に表示（元の画像サイズに対する相対座標）
            rect = self.get_rect()
            print(f'rect_start: {self.rect_start.x()}, {self.rect_start.y()}')
            print(f'rect_end: {self.rect_end.x()}, {self.rect_end.y()}')

            print(f'rect: {rect.x()}, {rect.y()}')
            # ラベルの位置とサイズを表示
            geometry = self.geometry()
            print(f"ラベルの位置: x={geometry.x()}, y={geometry.y()}")

            # スケール1.0での矩形を保存
            self.current_rect = self.scale_rect_to_original(rect)
            print(f"矩形の座標（元画像サイズに対する相対座標）: x1={self.current_rect.x()}, y1={self.current_rect.y()}, x2={self.current_rect.x() + self.current_rect.width()}, y2={self.current_rect.y() + self.current_rect.height()}")

            # 現在のスケールでの矩形を計算
            self.scaled_rect = QRect(
                int(self.current_rect.x() * self.scale),
                int(self.current_rect.y() * self.scale),
                int(self.current_rect.width() * self.scale),
                int(self.current_rect.height() * self.scale)
            )
            self.update()

class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_label = None
        self.selection_rect = None
        self.original_pixmap = None
        self.scale = 1.0
        self.scale_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        self.scale_index = 0
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
        layout.setContentsMargins(0, 0, 0, 0)  # マージンを0に設定
        layout.setSpacing(0)  # スペースを0に設定

        # 画像表示用のコンテナウィジェット
        container = QWidget()
        container.setLayout(QVBoxLayout())
        container.layout().setContentsMargins(0, 0, 0, 0)
        container.layout().setSpacing(0)

        self.image_label = ImageLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.image_label.setMouseTracking(True)
        self.image_label.setStyleSheet("background-color: rgb(0, 10, 30);")
        container.layout().addWidget(self.image_label)

        layout.addWidget(container)
        main_widget.setLayout(layout)

        # 選択矩形ウィジェットの設定
        self.selection_rect = SelectionRect(self.image_label)
        self.selection_rect.setGeometry(0, 0, 0, 0)  # 初期サイズを0に設定
        self.selection_rect.show()

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
            self.image_label.setScale(self.scale)  # スケール値を設定
            self.selection_rect.setScale(self.scale)  # 選択矩形にもスケールを設定

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.selection_rect and self.image_label:
            # ImageLabelの実際の位置とサイズを取得
            label_geometry = self.image_label.geometry()
            # SelectionRectの位置とサイズを更新
            self.selection_rect.setGeometry(label_geometry)
            print(f"ImageLabel geometry: {label_geometry.x()}, {label_geometry.y()}, {label_geometry.width()}, {label_geometry.height()}")
            print(f"SelectionRect geometry: {self.selection_rect.geometry().x()}, {self.selection_rect.geometry().y()}, {self.selection_rect.geometry().width()}, {self.selection_rect.geometry().height()}")

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
