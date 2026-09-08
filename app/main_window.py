import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QSlider, QGroupBox, QSpinBox,
    QSystemTrayIcon, QMenu, QAction, QDialog, QStyle
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from app.player import Player
from app.scheduler import TaskScheduler
from app.utils import set_autostart, parse_share_link

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于")
        self.setFixedSize(360, 230)
        self.setStyleSheet("""
            QDialog {
                background-color: #282828;
                border-radius: 16px;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', 'Microsoft YaHei';
            }
            QPushButton {
                background-color: #1DB954;
                border: none;
                border-radius: 20px;
                padding: 10px 28px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1ed760;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        title = QLabel("🎵 NeteaseTimer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        author = QLabel('作者: <span style="color:#1DB954;">Aiden Ormond</span>')
        author.setAlignment(Qt.AlignCenter)
        layout.addWidget(author)

        link = QLabel('<a href="https://github.com/Aiden-Ormond" style="color:#1DB954;">GitHub 发布页</a>')
        link.setOpenExternalLinks(True)
        link.setAlignment(Qt.AlignCenter)
        layout.addWidget(link)

        version = QLabel("版本 1.0 · 使用 Python + PyQt5")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color: #b3b3b3;")
        layout.addWidget(version)

        layout.addStretch()
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeteaseTimer")
        self.setMinimumSize(460, 550)
        self.setMaximumWidth(520)

        # 使用 Qt 内置标准图标作为窗口图标
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        # 全局暗色 Spotify 风格样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', 'Microsoft YaHei';
            }
            QLineEdit {
                background-color: #282828;
                border: 2px solid #535353;
                border-radius: 20px;
                padding: 10px 16px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #1DB954;
            }
            QPushButton {
                background-color: #1DB954;
                border: none;
                border-radius: 20px;
                padding: 10px 26px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1ed760;
            }
            QPushButton:pressed {
                background-color: #169c46;
            }
            QComboBox {
                background-color: #282828;
                border: 2px solid #535353;
                border-radius: 20px;
                padding: 8px 16px;
                color: #ffffff;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #1DB954;
                margin-right: 10px;
            }
            QCheckBox {
                spacing: 8px;
                color: #b3b3b3;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #535353;
                background: transparent;
            }
            QCheckBox::indicator:checked {
                background-color: #1DB954;
                border-color: #1DB954;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #535353;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #1DB954;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #1DB954;
                border-radius: 3px;
            }
            QGroupBox {
                border: none;
                margin-top: 12px;
                padding: 20px 16px 16px;
                background-color: #181818;
                border-radius: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                top: -8px;
                padding: 0 8px;
                color: #b3b3b3;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }
            QSpinBox {
                background-color: #282828;
                border: 2px solid #535353;
                border-radius: 16px;
                padding: 6px 12px;
                color: #ffffff;
                font-size: 13px;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)
        self.layout.setContentsMargins(20, 12, 20, 12)
        self.layout.setSpacing(14)

        # 标题
        title_label = QLabel("NeteaseTimer")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # 链接输入
        link_layout = QHBoxLayout()
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("粘贴网易云分享链接，自动解析")
        self.parse_btn = QPushButton("解析")
        self.parse_btn.setFixedWidth(80)
        self.parse_btn.clicked.connect(self.parse_link)
        link_layout.addWidget(self.link_input)
        link_layout.addWidget(self.parse_btn)
        self.layout.addLayout(link_layout)

        self.id_label = QLabel("尚未解析")
        self.id_label.setStyleSheet("color: #b3b3b3; font-size: 12px; margin-left: 8px;")
        self.layout.addWidget(self.id_label)

        # 周期选择
        period_group = QGroupBox("重复周期")
        period_layout = QVBoxLayout()
        period_layout.setContentsMargins(0,0,0,0)
        self.period_combo = QComboBox()
        self.period_combo.addItems(["仅一次", "每天", "工作日 (周一至周五)", "自定义"])
        self.period_combo.currentIndexChanged.connect(self.on_period_changed)
        period_layout.addWidget(self.period_combo)

        days_layout = QHBoxLayout()
        days_layout.setSpacing(4)
        self.day_checkboxes = []
        for day in ["周一","周二","周三","周四","周五","周六","周日"]:
            cb = QCheckBox(day)
            cb.setVisible(False)
            self.day_checkboxes.append(cb)
            days_layout.addWidget(cb)
        period_layout.addLayout(days_layout)
        period_group.setLayout(period_layout)
        self.layout.addWidget(period_group)

        # 时间与音量
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(14)

        time_group = QGroupBox("触发时间")
        time_inner = QHBoxLayout()
        self.hour_spin = QSpinBox()
        self.hour_spin.setRange(0,23)
        self.hour_spin.setPrefix("时 ")
        self.minute_spin = QSpinBox()
        self.minute_spin.setRange(0,59)
        self.minute_spin.setPrefix("分 ")
        time_inner.addWidget(self.hour_spin)
        time_inner.addWidget(self.minute_spin)
        time_inner.addStretch()
        time_group.setLayout(time_inner)
        controls_layout.addWidget(time_group)

        vol_group = QGroupBox("目标音量")
        vol_inner = QVBoxLayout()
        vol_slider_layout = QHBoxLayout()
        self.vol_slider = QSlider(Qt.Horizontal)
        self.vol_slider.setRange(0,100)
        self.vol_slider.setValue(50)
        self.vol_label = QLabel("50%")
        self.vol_label.setStyleSheet("color: #1DB954; font-weight: bold;")
        vol_slider_layout.addWidget(self.vol_slider)
        vol_slider_layout.addWidget(self.vol_label)
        self.vol_slider.valueChanged.connect(lambda v: self.vol_label.setText(f"{v}%"))
        vol_inner.addLayout(vol_slider_layout)

        gradual_layout = QHBoxLayout()
        gradual_layout.addWidget(QLabel("渐入时长(秒):"))
        self.gradual_spin = QSpinBox()
        self.gradual_spin.setRange(5,120)
        self.gradual_spin.setValue(30)
        gradual_layout.addWidget(self.gradual_spin)
        gradual_layout.addStretch()
        vol_inner.addLayout(gradual_layout)
        vol_group.setLayout(vol_inner)
        controls_layout.addWidget(vol_group)

        self.layout.addLayout(controls_layout)

        # 其他选项
        other_group = QGroupBox("其他")
        other_layout = QVBoxLayout()
        other_layout.setSpacing(8)

        self.autostart_cb = QCheckBox("开机自启")
        self.autostart_cb.stateChanged.connect(lambda s: set_autostart(s==2))
        other_layout.addWidget(self.autostart_cb)

        self.shutdown_cb = QCheckBox("播放结束后休眠电脑")
        other_layout.addWidget(self.shutdown_cb)

        shutdown_min_layout = QHBoxLayout()
        shutdown_min_layout.addWidget(QLabel("播放时长(分钟):"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1,999)
        self.duration_spin.setValue(30)
        shutdown_min_layout.addWidget(self.duration_spin)
        shutdown_min_layout.addStretch()
        other_layout.addLayout(shutdown_min_layout)

        other_group.setLayout(other_layout)
        self.layout.addWidget(other_group)

        # 按钮行
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.test_btn = QPushButton("▶ 立即测试")
        self.test_btn.setStyleSheet("background-color: #1DB954;")
        self.save_btn = QPushButton("💾 保存定时")
        self.save_btn.setStyleSheet("background-color: #535353; color: #ffffff;")
        self.about_btn = QPushButton("ℹ️ 关于")
        self.about_btn.setStyleSheet("background-color: transparent; border: 2px solid #535353; color: #b3b3b3;")
        btn_layout.addWidget(self.test_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.about_btn)
        self.layout.addLayout(btn_layout)

        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #b3b3b3; font-style: italic; margin-top: 8px;")
        self.layout.addWidget(self.status_label)

        # 连接信号
        self.test_btn.clicked.connect(self.test_now)
        self.save_btn.clicked.connect(self.save_timer)
        self.about_btn.clicked.connect(self.show_about)

        # 托盘
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        tray_menu = QMenu()
        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.showNormal)
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

        # 播放器和调度器
        self.player = Player()
        self.task_scheduler = TaskScheduler()

        # 窗口淡入动画
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(350)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_anim.start()

    # ---------- 槽函数 ----------
    def on_period_changed(self, idx):
        visible = (idx == 3)
        for cb in self.day_checkboxes:
            cb.setVisible(visible)

    def parse_link(self):
        url = self.link_input.text().strip()
        id_ = parse_share_link(url)
        if id_:
            self.id_label.setText(f"✅ 解析成功: ID = {id_}")
            self.current_target_id = id_
        else:
            self.id_label.setText("❌ 解析失败，请检查链接")
            self.current_target_id = None

    def test_now(self):
        if not hasattr(self, 'current_target_id') or not self.current_target_id:
            self.status_label.setText("⚠️ 请先解析链接")
            return
        vol = self.vol_slider.value() / 100.0
        gradual = self.gradual_spin.value()
        self.status_label.setText("🔊 正在播放...")
        self.player.alarm(self.current_target_id, volume=vol, gradual_duration=gradual)
        if self.shutdown_cb.isChecked():
            dur = self.duration_spin.value()
            self.player.shutdown_after(dur)
            self.status_label.setText(f"⏳ 将在 {dur} 分钟后休眠")

    def save_timer(self):
        hour = self.hour_spin.value()
        minute = self.minute_spin.value()
        time_str = f"{hour:02d}:{minute:02d}"
        period_idx = self.period_combo.currentIndex()
        if period_idx == 0:
            days = "once"
        elif period_idx == 1:
            days = "daily"
        elif period_idx == 2:
            days = "mon-fri"
        else:
            selected = [cb.text() for cb in self.day_checkboxes if cb.isChecked()]
            if not selected:
                self.status_label.setText("⚠️ 请选择至少一天")
                return
            mapping = {"周一":"MON","周二":"TUE","周三":"WED","周四":"THU","周五":"FRI","周六":"SAT","周日":"SUN"}
            days = ",".join(mapping[d] for d in selected)
        ok = TaskScheduler.create_wake_task(time_str, days)
        if ok:
            self.status_label.setText("✅ 定时任务已保存")
        else:
            self.status_label.setText("❌ 保存失败，请以管理员权限运行")

    def show_about(self):
        dlg = AboutDialog(self)
        dlg.exec_()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.activateWindow()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("NeteaseTimer", "程序已最小化到托盘", QSystemTrayIcon.Information, 1500)
