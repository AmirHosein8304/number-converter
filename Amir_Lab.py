import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QStackedWidget, QMessageBox, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve
from qt_material import apply_stylesheet


# ==== YOUR ORIGINAL LOGIC ====
def decimal_to_base(num, base):
    num = abs(num)
    if num == 0:
        return "0"
    digits = []
    while num:
        if num % base >= 10:
            digits.append(chr(ord('A') + num % base - 10))
        else:
            digits.append(str(num % base))
        num //= base
    return "".join(digits[::-1])

def base_to_decimal(num_str, base):
    num_str = str(num_str)
    if not num_str:
        return 0
    is_negative = num_str[0] == "-"
    if is_negative:
        num_str = num_str[1:]
    decimal = 0
    for digit in num_str:
        if digit.isdigit():
            value = int(digit)
        else:
            value = ord(digit.upper()) - ord('A') + 10
        if value >= base:
            raise ValueError(f"Invalid digit {digit} for base {base}")
        decimal = decimal * base + value
    return -decimal if is_negative else decimal

def convert_between_bases(num_str, from_base, to_base):
    decimal = base_to_decimal(num_str, from_base)
    return decimal_to_base(decimal, to_base)

def two_complement(num, k):
    num = base_to_decimal(num, 2)
    result = 2**k - num
    return decimal_to_base(result, 2)


# ==== MODERN STYLED GUI ====
class ModernConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ Number Converter & 2's Complement")
        self.setGeometry(300, 150, 550, 400)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.option_combo = QComboBox()
        self.option_combo.addItems(["🔘 Choose Option", "🧮 Base Converter", "⚙️ 2's Complement"])
        self.option_combo.currentIndexChanged.connect(self.switch_option)
        self.main_layout.addWidget(self.option_combo)

        # Fancy stacked area
        self.stack = QStackedWidget()
        self.stack.addWidget(QWidget())  # Placeholder
        self.stack.addWidget(self.create_converter_panel())
        self.stack.addWidget(self.create_twos_panel())
        self.main_layout.addWidget(self.stack)

    def create_converter_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        self.num_input = QLineEdit()
        self.from_base = QLineEdit()
        self.to_base = QLineEdit()
        self.convert_result = QLabel("Result will appear here 🚀")

        for field in [self.num_input, self.from_base, self.to_base]:
            field.setPlaceholderText("Enter value...")
            field.setStyleSheet("padding: 10px; font-size: 16px;")

        convert_btn = QPushButton("🔁 Convert Base")
        convert_btn.clicked.connect(self.run_base_converter)

        self.convert_result.setStyleSheet(
            "padding: 12px; border: 2px solid #00BCD4; border-radius: 8px; background-color: #E0F7FA;"
            "font-size: 16px; font-weight: bold; color: #006064;"
        )

        layout.addWidget(QLabel("🔢 Number:"))
        layout.addWidget(self.num_input)
        layout.addWidget(QLabel("📥 From Base:"))
        layout.addWidget(self.from_base)
        layout.addWidget(QLabel("📤 To Base:"))
        layout.addWidget(self.to_base)
        layout.addWidget(convert_btn)
        layout.addWidget(self.convert_result)
        panel.setLayout(layout)
        return panel

    def create_twos_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        self.twos_input = QLineEdit()
        self.twos_bits = QLineEdit()
        self.twos_result = QLabel("2's complement will appear here 💡")

        for field in [self.twos_input, self.twos_bits]:
            field.setPlaceholderText("Enter binary or bit length...")
            field.setStyleSheet("padding: 10px; font-size: 16px;")

        run_btn = QPushButton("🧮 Calculate 2's Complement")
        run_btn.clicked.connect(self.run_twos_complement)

        self.twos_result.setStyleSheet(
            "padding: 12px; border: 2px solid #FF5722; border-radius: 8px; background-color: #FFE0B2;"
            "font-size: 16px; font-weight: bold; color: #BF360C;"
        )

        layout.addWidget(QLabel("💻 Binary Number:"))
        layout.addWidget(self.twos_input)
        layout.addWidget(QLabel("📏 Number of Bits (k):"))
        layout.addWidget(self.twos_bits)
        layout.addWidget(run_btn)
        layout.addWidget(self.twos_result)
        panel.setLayout(layout)
        return panel

    def switch_option(self, index):
        self.stack.setCurrentIndex(index)

    def run_base_converter(self):
        try:
            num = self.num_input.text()
            from_b = int(self.from_base.text())
            to_b = int(self.to_base.text())
            result = convert_between_bases(num, from_b, to_b)
            self.convert_result.setText(f"✅ Result: {result}")
        except Exception as e:
            QMessageBox.critical(self, "Conversion Error", str(e))

    def run_twos_complement(self):
        try:
            num = self.twos_input.text()
            k = int(self.twos_bits.text())
            result = two_complement(num, k)
            self.twos_result.setText(f"✅ 2's Complement: {result}")
        except Exception as e:
            QMessageBox.critical(self, "2's Complement Error", str(e))


# === RUN ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')  # <== super slick dark theme
    window = ModernConverter()
    window.show()
    sys.exit(app.exec_())
