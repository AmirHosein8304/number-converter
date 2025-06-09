import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QStackedWidget, QMessageBox
)

# Your original functions
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

# GUI Panel
class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base Converter & 2's Complement Tool")
        self.setGeometry(300, 200, 400, 250)

        self.layout = QVBoxLayout()

        # Dropdown to choose option
        self.option_select = QComboBox()
        self.option_select.addItems(["Select Option", "1: Base Converter", "2: 2's Complement"])
        self.option_select.currentIndexChanged.connect(self.switch_panel)
        self.layout.addWidget(self.option_select)

        # Panels
        self.stack = QStackedWidget()
        self.stack.addWidget(QWidget())  # Empty placeholder
        self.stack.addWidget(self.create_base_converter_panel())
        self.stack.addWidget(self.create_twos_complement_panel())
        self.layout.addWidget(self.stack)

        self.setLayout(self.layout)

    def create_base_converter_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        self.input_num = QLineEdit()
        self.from_base = QLineEdit()
        self.to_base = QLineEdit()
        self.result_base = QLabel("Result: ")

        convert_btn = QPushButton("Convert")
        convert_btn.clicked.connect(self.run_base_converter)

        layout.addWidget(QLabel("Number:"))
        layout.addWidget(self.input_num)
        layout.addWidget(QLabel("From Base:"))
        layout.addWidget(self.from_base)
        layout.addWidget(QLabel("To Base:"))
        layout.addWidget(self.to_base)
        layout.addWidget(convert_btn)
        layout.addWidget(self.result_base)

        panel.setLayout(layout)
        return panel

    def create_twos_complement_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        self.input_twos = QLineEdit()
        self.input_bits = QLineEdit()
        self.result_twos = QLabel("Result: ")

        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.run_twos_complement)

        layout.addWidget(QLabel("Binary Number:"))
        layout.addWidget(self.input_twos)
        layout.addWidget(QLabel("Number of Bits (k):"))
        layout.addWidget(self.input_bits)
        layout.addWidget(calc_btn)
        layout.addWidget(self.result_twos)

        panel.setLayout(layout)
        return panel

    def switch_panel(self, index):
        self.stack.setCurrentIndex(index)

    def run_base_converter(self):
        try:
            num = self.input_num.text()
            from_b = int(self.from_base.text())
            to_b = int(self.to_base.text())
            result = convert_between_bases(num, from_b, to_b)
            self.result_base.setText(f"Result: {result}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def run_twos_complement(self):
        try:
            num = self.input_twos.text()
            k = int(self.input_bits.text())
            result = two_complement(num, k)
            self.result_twos.setText(f"Result: {result}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
