import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy,
    QProgressBar, QToolTip,QDialog
)
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize, QTimer

from checker.common import load_common_passwords
from checker.complexity import give_suggestions
from checker.strength import calculate_password_strength, display_strength, is_breached


class PasswordCheckerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Strength Checker")
        self.setGeometry(400, 200, 550, 550)
        self.setWindowIcon(QIcon("Data/app_icon.png"))  # Add your app icon here

        # Dark theme background
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(18, 18, 18))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        self.common_passwords = load_common_passwords("data/weak_passwords.txt")

        self.init_ui()

        # Timer for debounce typing event
        self.typing_timer = QTimer()
        self.typing_timer.setSingleShot(True)
        self.typing_timer.timeout.connect(self.on_password_input_stopped)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title
        title = QLabel("🔒 Password Strength Checker")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #00cc66;")
        layout.addWidget(title)

        # Info image
        info_image = QLabel()
        info_image.setAlignment(Qt.AlignCenter)
        info_image.setPixmap(QPixmap("Data/pass_strong.jpeg").scaledToWidth(380, Qt.SmoothTransformation))
        layout.addWidget(info_image)

        # Password + Eye icon row
        password_row = QHBoxLayout()
        password_row.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 14))
        self.password_input.setFixedWidth(350)
        self.password_input.setStyleSheet("""
            padding: 12px;
            border: 2px solid #00cc66;
            border-radius: 10px;
            color: white;
            background-color: #111;
            selection-background-color: #00cc66;
        """)
        self.password_input.textChanged.connect(self.on_password_typing)

        # Eye icon button
        self.toggle_eye_btn = QPushButton()
        self.toggle_eye_btn.setCheckable(True)
        self.toggle_eye_btn.setIcon(QIcon("Data/eye_icon.png"))
        self.toggle_eye_btn.setIconSize(QSize(28, 28))
        self.toggle_eye_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_eye_btn.setToolTip("Show/Hide Password")
        self.toggle_eye_btn.setStyleSheet("background-color: transparent; border: none;")
        self.toggle_eye_btn.clicked.connect(self.toggle_password_visibility)

        password_row.addWidget(self.password_input)
        password_row.addWidget(self.toggle_eye_btn)
        password_row.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(password_row)

        # Progress bar for strength
        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximum(17)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedWidth(420)
        self.strength_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00cc66;
                border-radius: 10px;
                background-color: #222;
            }
            QProgressBar::chunk {
                background-color: #00cc66;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.strength_bar, alignment=Qt.AlignCenter)

        # Check button
        btn = QPushButton("Check If Password is Breached..")
        btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #00cc66;
                color: black;
                padding: 12px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #009944;
            }
        """)
        btn.clicked.connect(self.check_password)

        # Center button layout with margins
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(btn)
        btn_layout.addStretch(1)
        btn_layout.setContentsMargins(30, 0, 30, 0)
        layout.addLayout(btn_layout)

        # Results label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont("Segoe UI", 14))
        self.result_label.setStyleSheet("color: white;")
        layout.addWidget(self.result_label)

        # Suggestions label
        self.suggestions_label = QLabel("")
        self.suggestions_label.setAlignment(Qt.AlignLeft)
        self.suggestions_label.setWordWrap(True)
        self.suggestions_label.setFont(QFont("Segoe UI", 12))
        self.suggestions_label.setStyleSheet("color: white;")
        layout.addWidget(self.suggestions_label)

        self.setLayout(layout)

    def on_password_typing(self):
        # Restart debounce timer on every key press
        self.typing_timer.start(100)  # 600ms delay after last key press

    def on_password_input_stopped(self):
        # Auto-check password strength & suggestions as user stops typing
        password = self.password_input.text().strip()
        if password:
            self.check_password(auto=True)

    def toggle_password_visibility(self):
        if self.toggle_eye_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_eye_btn.setIcon(QIcon("Data/eye_off.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_eye_btn.setIcon(QIcon("Data/eye_icon.png"))

    def show_breach_warning(self, count):
        dialog = QDialog(self)
        dialog.setWindowTitle("⚠ Breached Password Warning ⚠")
        dialog.setModal(True)
        dialog.resize(450, 220)

        # Dark red background for urgency
        palette = dialog.palette()
        palette.setColor(dialog.backgroundRole(), QColor(60, 0, 0))
        dialog.setPalette(palette)

        layout = QVBoxLayout()

        # Large bold warning label
        warning_label = QLabel("⚠ WARNING! PASSWORD BREACHED ⚠")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        warning_label.setStyleSheet("color: #FF4444;")
        layout.addWidget(warning_label)

        # Breach details label
        detail_label = QLabel(
            f"This password has been found in <b><span style='color: yellow;'>{count}</span></b> data breaches.\n\n"
            "For your security, please choose a stronger password."
        )
        detail_label.setAlignment(Qt.AlignCenter)
        detail_label.setFont(QFont("Segoe UI", 16))
        detail_label.setStyleSheet("color: white;")
        layout.addWidget(detail_label)

        dialog.setLayout(layout)
        dialog.exec_()

    def check_password(self, auto=False):
        password = self.password_input.text().strip()

        if not password:
            if not auto:
                QMessageBox.warning(self, "Input Error", "Password cannot be empty.")
            self.result_label.setText("")
            self.suggestions_label.setText("")
            self.strength_bar.setValue(0)
            return

        if not auto:
            self.result_label.setText("<i>Checking breach database...</i>")
            QApplication.processEvents()

            try:
                breached, count = is_breached(password)
            except ConnectionError:
                breached, count = None, None

            if breached:
                self.show_breach_warning(count)  # Use custom big warning dialog here
                self.result_label.setText("")
                self.suggestions_label.setText("")
                self.strength_bar.setValue(0)
                return
        else:
            breached, count = None, None  # Skip breach check on auto

        # Continue with strength evaluation
        points = calculate_password_strength(password, self.common_passwords)
        strength_text = display_strength(points)
        color = {
            "Very Weak": "red",
            "Weak": "orange",
            "Good": "#F1C40F",
            "Strong": "lime"
        }.get(strength_text, "white")

        self.result_label.setText(
            f"<b>Points:</b> {points}<br>"
            f"<b>Strength:</b> <span style='color:{color}; font-weight:bold;'>{strength_text}</span>"
        )
        self.strength_bar.setValue(points)

        suggestions = give_suggestions(password)
        if suggestions:
            formatted = "<br>".join(f"• {s}" for s in suggestions)
            self.suggestions_label.setText(f"<b>Suggestions:</b><br>{formatted}")
        else:
            self.suggestions_label.setText("<b>Suggestions:</b> ✅ Looks good!")


def run_app():
    app = QApplication(sys.argv)
    window = PasswordCheckerWindow()
    window.show()
    sys.exit(app.exec_())
