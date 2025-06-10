from math import log
import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QStackedWidget, QFrame, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QPen, QFontDatabase

# === Your Logic (with Overflow Check) ===
def decimal_to_base(num, base, k, d=0):
    if k==0:
        k = int(log(num,base)) + 1
    if k < d:
        return "Overflow!"
    f = False
    if num % 1 != 0:
        f = True
    if num <= 0:
        num = two_complement(abs(num), k)
    if num == 0:
        return "0"
    if not f:
        digits = [0] * k
    else:
        digits = [0] * (k - d)
    while num >= 1:
        try:
            digits[k - d - 1 - int(log(num, base))] = int(num // (base ** int(log(num, base))))
            num = num % (base ** int(log(num, base)))
        except IndexError:
            return "Overflow!"
    if num:
        f_digits = [0] * d
        for i in range(d):
            if num == 0:
                break
            f_digits[abs(int(log(num, base))) - 1] = int(num // (base ** int(log(num, base))))
            num = num % (base ** int(log(num, base)))
        digits.extend(f_digits)
    
    return "".join(map(str, digits))

def base_to_decimal(num_str, base, k, d=0):
    num_str = list(str(num_str))
    if not num_str:
        return 0
    decimal = 0
    if d:
        f_digits = num_str[k-d:k]
        num_str = num_str[:k-d]
        for i in range(d):
            if f_digits[i].isdigit():
                value = int(f_digits[i])
            else:
                value = ord(f_digits[i].upper()) - ord('A') + 10
            decimal += value * base **(-i-1)
    for i in range(k-d):
        if num_str[i].isdigit():
            value = int(num_str[i])
        else:
            value = ord(num_str[i].upper()) - ord('A') + 10
        if value >= base:
            raise ValueError(f"Invalid digit {num_str[i]} for base {base}")
        decimal += value * base ** (k - d - i - 1)
    return decimal

def convert_between_bases(num_str, from_base, to_base, k, d1=0, d2=0):
    decimal = base_to_decimal(num_str, from_base, len(str(num_str)), d1)
    return decimal_to_base(decimal, to_base, k, d2)

def two_complement(num, k):
    # This function expects a binary string input
    decimal_val = base_to_decimal(num, 2)
    if decimal_val >= 2**k:
        return "Overflow" # Can't take complement of number that already exceeds k bits
    
    # Standard 2's complement calculation for a positive number
    result = 2**k - decimal_val
    return decimal_to_base(result, 2, k)

# === Background Rain (unchanged) ===
class MovingSymbolsBackground(QFrame):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_symbols)
        self.timer.start(50)

        self.symbols = ["%","&","8","0", "1", "+", "-", "=", "/", "*", "^"]
        self.positions = [self.random_position() for _ in range(60)]
        self.colors = [
            QColor(57, 255, 20), QColor(255, 20, 147), QColor(0, 255, 255),
            QColor(255, 69, 0), QColor(138, 43, 226), QColor(0, 191, 255),
            QColor(255, 255, 0), QColor(255, 0, 255), QColor(240, 230, 140)
        ]
        self.symbol_colors = [random.choice(self.colors) for _ in self.positions]

    def random_position(self):
        return [random.randint(0, self.width()), random.randint(0, self.height()), random.choice(self.symbols)]

    def update_symbols(self):
        for i, pos in enumerate(self.positions):
            pos[1] += 4
            if pos[1] > self.height():
                pos[0] = random.randint(0, self.width())
                pos[1] = 0
                pos[2] = random.choice(self.symbols)
                self.symbol_colors[i] = random.choice(self.colors)
        self.update()

    def resizeEvent(self, event):
        self.positions = [self.random_position() for _ in range(60)]
        self.symbol_colors = [random.choice(self.colors) for _ in self.positions]

    def paintEvent(self, event):
        painter = QPainter(self)
        font = QFont("Orbitron", 20, QFont.Bold)
        painter.setFont(font)
        for i, (x, y, char) in enumerate(self.positions):
            painter.setPen(QPen(self.symbol_colors[i]))
            painter.drawText(x, y, char)

# === Main App (GUI updated) ===
class DynamicConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        font_id = QFontDatabase.addApplicationFont("fonts/Orbitron-Regular.ttf")
        self.cyberpunk_font_family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Orbitron"
        self.setWindowTitle("Number Conversion Tool")
        self.setGeometry(200, 100, 800, 400)
        self.stack = QStackedWidget()
        self.main_menu = self.create_main_menu()
        self.base_panel = self.create_base_panel()
        self.twos_panel = self.create_twos_panel()
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.base_panel)
        self.stack.addWidget(self.twos_panel)
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
        self.apply_dynamic_style()

    def apply_dynamic_style(self):
        self.setStyleSheet(f"""
            QWidget {{ background-color: #0f0c29; font-family: '{self.cyberpunk_font_family}', Courier, monospace; color: white; }}
            QLineEdit, QPushButton {{ font-size: 18px; padding: 10px; border-radius: 6px; font-family: '{self.cyberpunk_font_family}', Courier, monospace; }}
            QPushButton {{ background-color: #673AB7; color: white; font-weight: bold; }}
            QPushButton:hover {{ background-color: #9575CD; }}
            QLabel {{ font-family: '{self.cyberpunk_font_family}', Courier, monospace; }}
        """)

    def create_main_menu(self):
        panel = MovingSymbolsBackground()
        layout = QVBoxLayout()
        title = QLabel("Choose an Option")
        title.setFont(QFont(self.cyberpunk_font_family, 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        btn_base = QPushButton("Base Converter")
        btn_base.clicked.connect(lambda: self.stack.setCurrentWidget(self.base_panel))
        btn_twos = QPushButton("2's Complement Calculator")
        btn_twos.clicked.connect(lambda: self.stack.setCurrentWidget(self.twos_panel))
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(btn_base)
        layout.addWidget(btn_twos)
        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def create_base_panel(self):
        panel = MovingSymbolsBackground()
        layout = QVBoxLayout()
        title = QLabel("Base Converter")
        title.setFont(QFont(self.cyberpunk_font_family, 18, QFont.Bold))
        self.input_number = QLineEdit()
        self.input_number.setPlaceholderText("Enter Number")
        self.input_from = QLineEdit()
        self.input_from.setPlaceholderText("From Base")
        self.input_to = QLineEdit()
        self.input_to.setPlaceholderText("To Base")

        # --- NEW WIDGET ---
        # Added a QLineEdit for the user to input the number of bits (k).
        self.input_k_base = QLineEdit()
        self.input_k_base.setPlaceholderText("Number of Bits (k) - Optional")

        self.checkbox_signed = QCheckBox("Is your number signed?")
        self.checkbox_decimal = QCheckBox("Is your number decimal?")
        self.checkbox_decimal.stateChanged.connect(self.toggle_decimal_digits_input)
        self.input_decimal_digits = QLineEdit()
        self.input_decimal_digits.setPlaceholderText("Digits after decimal")
        self.input_decimal_digits.setVisible(False)
        self.result_base = QLabel("Result will appear here")
        self.result_base.setWordWrap(True)
        btn = QPushButton("Convert")
        btn.clicked.connect(self.run_base_conversion)
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))

        layout.addWidget(title)
        layout.addWidget(self.input_number)
        layout.addWidget(self.input_from)
        layout.addWidget(self.input_to)
        # --- ADDED WIDGET TO LAYOUT ---
        layout.addWidget(self.input_k_base)
        layout.addWidget(self.checkbox_signed)
        layout.addWidget(self.checkbox_decimal)
        layout.addWidget(self.input_decimal_digits)
        layout.addWidget(btn)
        layout.addWidget(self.result_base)
        layout.addWidget(back_btn)
        panel.setLayout(layout)
        return panel

    def toggle_decimal_digits_input(self, state):
        self.input_decimal_digits.setVisible(state == Qt.Checked)

    # MODIFIED: Logic to get K and handle the "Overflow" return string.
    def run_base_conversion(self):
        try:
            num_str = self.input_number.text()
            from_b = int(self.input_from.text())
            to_b = int(self.input_to.text())
            
            # Get k from the new input field. Default to 0 if empty.
            k_text = self.input_k_base.text()
            k = int(k_text) if k_text else 0

            is_signed = self.checkbox_signed.isChecked()
            is_decimal = self.checkbox_decimal.isChecked()

            if not is_signed and num_str.startswith("-"):
                raise ValueError("Sign not allowed for unsigned number.")

            # This part for decimal/fractional numbers remains unchanged
            if is_decimal:
                # (Your existing logic for fractional numbers)
                digits_after = int(self.input_decimal_digits.text())
                if "." in num_str:
                    whole, frac = num_str.split(".")
                    dec_value = base_to_decimal(whole, from_b)
                    frac_value = sum(
                        base_to_decimal(ch, from_b) * (from_b ** -(i + 1))
                        for i, ch in enumerate(frac)
                    )
                    final_decimal = dec_value + frac_value
                else:
                    final_decimal = base_to_decimal(num_str, from_b)

                int_part = int(final_decimal)
                frac_part = final_decimal - int_part
                
                # Pass k to the integer part conversion
                converted_int = decimal_to_base(int_part, to_b, k)
                if converted_int == "Overflow":
                    raise ValueError("Overflow in integer part")

                result = converted_int
                if frac_part > 0:
                    result += "."
                    for _ in range(digits_after):
                        frac_part *= to_b
                        digit = int(frac_part)
                        result += decimal_to_base(digit, to_b, 0) # k=0 for single digits
                        frac_part -= digit
            else:
                # Pass k to the main conversion function
                result = convert_between_bases(num_str, from_b, to_b, k)

            # --- DISPLAY OVERFLOW ---
            # Check if the function returned the specific "Overflow" error string.
            if result == "Overflow":
                self.result_base.setText("Error: Overflow")
            else:
                self.result_base.setText(f"Result: {result}")
        except Exception as e:
            self.result_base.setText(f"Error: {str(e)}")


    def create_twos_panel(self):
        panel = MovingSymbolsBackground()
        layout = QVBoxLayout()
        title = QLabel("2's Complement Calculator")
        title.setFont(QFont(self.cyberpunk_font_family, 18, QFont.Bold))
        self.input_bin = QLineEdit()
        self.input_bin.setPlaceholderText("Enter Binary Number")
        self.input_k = QLineEdit()
        self.input_k.setPlaceholderText("Number of Bits (k)")
        self.result_twos = QLabel("Result will appear here")
        self.result_twos.setWordWrap(True)
        btn = QPushButton("Calculate")
        btn.clicked.connect(self.run_twos_complement)
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))
        layout.addWidget(title)
        layout.addWidget(self.input_bin)
        layout.addWidget(self.input_k)
        layout.addWidget(btn)
        layout.addWidget(self.result_twos)
        layout.addWidget(back_btn)
        panel.setLayout(layout)
        return panel

    # MODIFIED: To handle overflow from the logic function
    def run_twos_complement(self):
        try:
            num = self.input_bin.text()
            k = int(self.input_k.text())
            result = two_complement(num, k)

            if result == "Overflow":
                self.result_twos.setText("Error: Overflow")
            else:
                self.result_twos.setText(f"2's Complement: {result}")

        except Exception as e:
            self.result_twos.setText(f"Error: {str(e)}")

# === App Execution ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicConverterApp()
    window.show()
    sys.exit(app.exec_())