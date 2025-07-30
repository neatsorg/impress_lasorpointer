import os
import sys

from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QColor, QCursor, QGuiApplication, QPainter
from PyQt5.QtWidgets import QApplication, QWidget

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"

app = QApplication([])

# すべての画面を取得
screens = QGuiApplication.screens()

# セカンダリモニタの情報（右側にあるとする）
if len(screens) >= 2:
    secondary = max(screens, key=lambda s: s.geometry().x())  # ← 念のため右端の画面に固定
    geometry = secondary.geometry()
    SECONDARY_OFFSET_X = geometry.x()
    SECONDARY_RESOLUTION = (geometry.width(), geometry.height())
else:
    print("セカンダリディスプレイが見つかりません。終了します。")
    sys.exit(1)

# 発表者ツール内の白枠の位置とサイズ（モニタ1側の白枠の位置とサイズ。仮）
WHITE_FRAME_X = 50
WHITE_FRAME_Y = 230
WHITE_FRAME_WIDTH = 1100
WHITE_FRAME_HEIGHT = 620

# 縦方向補正
Y_OFFSET_CORRECTION = 0  # ← 必要に応じて調整

class LaserPointerOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.setGeometry(SECONDARY_OFFSET_X, 0, *SECONDARY_RESOLUTION)
        self.pointer_pos = QPoint(-100, -100)
        self.radius = 20

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pointer)
        self.timer.start(16)

        self.show()

    def update_pointer(self):
        global_pos = QCursor.pos()
        gx, gy = global_pos.x(), global_pos.y()

        if (WHITE_FRAME_X <= gx <= WHITE_FRAME_X + WHITE_FRAME_WIDTH and
            WHITE_FRAME_Y <= gy <= WHITE_FRAME_Y + WHITE_FRAME_HEIGHT):
            
            rel_x = (gx - WHITE_FRAME_X) / WHITE_FRAME_WIDTH
            rel_y = (gy - WHITE_FRAME_Y) / WHITE_FRAME_HEIGHT

            new_x = int(rel_x * SECONDARY_RESOLUTION[0])
            new_y = int(rel_y * SECONDARY_RESOLUTION[1]) + Y_OFFSET_CORRECTION

            self.pointer_pos = QPoint(new_x, new_y)
        else:
            self.pointer_pos = QPoint(-100, -100)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(255, 0, 0, 180)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            self.pointer_pos.x() - self.radius,
            self.pointer_pos.y() - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

if __name__ == "__main__":
    overlay = LaserPointerOverlay()
    sys.exit(app.exec_())
