from math import log,ceil
import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QStackedWidget, QFrame, QCheckBox, QRadioButton, QButtonGroup, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QPen, QFontDatabase

# === Your Logic (with Overflow Check) ===
def decimal_to_base(num, base, k=None, d=0, u=False):
    if base>36:
        raise ValueError("Invalid base")
    flag = False
    if base != 2 and u:
        raise ValueError("Invalid base for two's complement")
    num = float(num)
    #c = -1 if num % 1 != 0 else 0
    if not k:
        flag = True
        k = ceil(log(abs(num), base)) + d + 1 if u else ceil(log(num, base)) + d
    if u and num <= 0 and base==2:
        return two_complement(abs(num), k-d, d, True)
    if k < d:
        return "Overflow!"
    if num == 0:
        return "0"
    digits = [0] * (k-d)
    while num >= 1:
        try:
            digits[k - d - 1 - int(log(num, base))] = int(num // (base ** int(log(num, base))))
            if digits[k - d - 1 - int(log(num, base))] >= 9:
                digits[k - d - 1 - int(log(num, base))] = chr(ord('A') + digits[k - d - 1 - int(log(num, base))] - 10)
                try:
                    digits.pop(k-d-int(log(num,base)))
                except:
                    pass
            num = num % (base ** int(log(num, base)))
        except IndexError:
            return "Overflow!"
    if num:
        f_digits = [0] * d
        for i in range(d):
            if num == 0:
                break
            try:
                if num<0:
                    f_digits[abs(int(log(abs(num), base))) - 1] = int(num // (base ** int(log(num, base)-1)))
                else:
                    f_digits[abs(int(log(abs(num), base))) - 1] = int(num // (base ** int(log(num, base))))
            except:
                break
            num = num % (base ** int(log(num, base)))
        digits.extend(f_digits)
    
    return "".join(map(str, digits))

def base_to_decimal(num_str, base, k=None, d=0,u=False):
    num_str = list(str(num_str))
    if not k:
        k = len(num_str)
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
    if u and decimal >= 2**(k-d-1):
        decimal -= 2**(k-d)
    return decimal

def convert_between_bases(num_str, from_base, to_base, k, d1=0, d2=0, u=False):
    decimal = base_to_decimal(num_str, from_base, len(str(num_str)), d1, u) if from_base != 10 else float(num_str)
    if to_base == 10:
        return str(round(decimal,d2))
    return decimal_to_base(decimal, to_base, k, d2, u) if decimal != "Overflow!" else decimal

def two_complement(num, k ,d , n=False):
    if num >= 2**k:
        return "Overflow!"
    result = 2**k - num if n else num
    return decimal_to_base(result, 2, k+d, d)

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
        self.add_subtract_panel = self.create_add_subtract_panel()  # New panel
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.base_panel)
        self.stack.addWidget(self.twos_panel)
        self.stack.addWidget(self.add_subtract_panel)  # Add new panel to stack
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
            QRadioButton {{ font-size: 16px; padding: 5px; }}
            QGroupBox {{ font-size: 16px; margin-top: 10px; border: 1px solid #673AB7; border-radius: 5px; padding: 10px; }}
            QGroupBox::title {{ subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }}
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
        
        # Add new button for Add/Subtract
        btn_add_sub = QPushButton("Add / Subtract")
        btn_add_sub.clicked.connect(lambda: self.stack.setCurrentWidget(self.add_subtract_panel))
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(btn_base)
        layout.addWidget(btn_twos)
        layout.addWidget(btn_add_sub)  # Add new button to layout
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

        self.input_k_base = QLineEdit()
        self.input_k_base.setPlaceholderText("Number of Bits (k) - Optional")

        self.checkbox_signed = QCheckBox("Is your number signed?")
        self.checkbox_decimal = QCheckBox("Is your number decimal?")
        self.checkbox_decimal.stateChanged.connect(self.toggle_decimal_digits_input)

        # ✨ NEW INPUT FIELDS
        self.input_decimal_whole_digits = QLineEdit()
        self.input_decimal_whole_digits.setPlaceholderText("Digits to treat as decimal (d0)")
        self.input_decimal_digits = QLineEdit()
        self.input_decimal_digits.setPlaceholderText("Digits after conversion (d1)")

        self.input_decimal_whole_digits.setVisible(False)
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
        layout.addWidget(self.input_k_base)
        layout.addWidget(self.checkbox_signed)
        layout.addWidget(self.checkbox_decimal)
        layout.addWidget(self.input_decimal_whole_digits)  # d0
        layout.addWidget(self.input_decimal_digits)        # d1
        layout.addWidget(btn)
        layout.addWidget(self.result_base)
        layout.addWidget(back_btn)
        panel.setLayout(layout)
        return panel

    def toggle_decimal_digits_input(self, state):
        show = state == Qt.Checked
        self.input_decimal_digits.setVisible(show)
        self.input_decimal_whole_digits.setVisible(show)

    def run_base_conversion(self):
        try:
            num_str = self.input_number.text()
            from_b = int(self.input_from.text())
            to_b = int(self.input_to.text())
            k_text = self.input_k_base.text()
            k = int(k_text) if k_text else 0

            is_signed = self.checkbox_signed.isChecked()
            is_decimal = self.checkbox_decimal.isChecked()

            if not is_signed and num_str.startswith("-"):
                raise ValueError("Sign not allowed for unsigned number.")

            if is_decimal:
                d0 = int(self.input_decimal_whole_digits.text())
                d1 = int(self.input_decimal_digits.text())
                result = convert_between_bases(num_str, from_b, to_b, k, d1=d0, d2=d1, u=is_signed)
            else:
                result = convert_between_bases(num_str, from_b, to_b, k, u=is_signed)

            if result == "Overflow!":
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

            if result == "Overflow!":
                self.result_twos.setText("Error: Overflow")
            else:
                self.result_twos.setText(f"2's Complement: {result}")

        except Exception as e:
            self.result_twos.setText(f"Error: {str(e)}")
            
    # New method for Add/Subtract panel
    def create_add_subtract_panel(self):
        panel = MovingSymbolsBackground()
        layout = QVBoxLayout()
        
        title = QLabel("Add / Subtract Calculator")
        title.setFont(QFont(self.cyberpunk_font_family, 18, QFont.Bold))
        layout.addWidget(title)
        
        # Number 1 input group
        num1_layout = QVBoxLayout()
        num1_label = QLabel("First Number (Binary):")
        self.num1_input = QLineEdit()
        self.num1_input.setPlaceholderText("Enter binary number")
        
        # Decimal options for number 1
        num1_dec_layout = QHBoxLayout()
        self.num1_decimal_cb = QCheckBox("Is it decimal?")
        self.num1_decimal_cb.stateChanged.connect(lambda: self.toggle_decimal_input(self.num1_digits_input))
        num1_dec_layout.addWidget(self.num1_decimal_cb)
        
        self.num1_digits_input = QLineEdit()
        self.num1_digits_input.setPlaceholderText("Decimal digits count")
        self.num1_digits_input.setVisible(False)
        num1_dec_layout.addWidget(self.num1_digits_input)
        
        num1_layout.addWidget(num1_label)
        num1_layout.addWidget(self.num1_input)
        num1_layout.addLayout(num1_dec_layout)
        layout.addLayout(num1_layout)
        
        # Number 2 input group
        num2_layout = QVBoxLayout()
        num2_label = QLabel("Second Number (Binary):")
        self.num2_input = QLineEdit()
        self.num2_input.setPlaceholderText("Enter binary number")
        
        # Decimal options for number 2
        num2_dec_layout = QHBoxLayout()
        self.num2_decimal_cb = QCheckBox("Is it decimal?")
        self.num2_decimal_cb.stateChanged.connect(lambda: self.toggle_decimal_input(self.num2_digits_input))
        num2_dec_layout.addWidget(self.num2_decimal_cb)
        
        self.num2_digits_input = QLineEdit()
        self.num2_digits_input.setPlaceholderText("Decimal digits count")
        self.num2_digits_input.setVisible(False)
        num2_dec_layout.addWidget(self.num2_digits_input)
        
        num2_layout.addWidget(num2_label)
        num2_layout.addWidget(self.num2_input)
        num2_layout.addLayout(num2_dec_layout)
        layout.addLayout(num2_layout)
        
        # Operation selection
        op_layout = QVBoxLayout()
        op_label = QLabel("Select Operation:")
        op_label.setFont(QFont(self.cyberpunk_font_family, 12))
        op_layout.addWidget(op_label)
        
        self.op_group = QButtonGroup(panel)
        self.add_radio = QRadioButton("Add")
        self.sub_radio = QRadioButton("Subtract")
        self.add_radio.setChecked(True)  # Default to Add
        
        op_layout.addWidget(self.add_radio)
        op_layout.addWidget(self.sub_radio)
        self.op_group.addButton(self.add_radio)
        self.op_group.addButton(self.sub_radio)
        
        layout.addLayout(op_layout)
        
        # Calculate button
        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.calculate_add_sub)
        layout.addWidget(calc_btn)
        
        # Result display
        self.add_sub_result = QLabel("Result will appear here")
        self.add_sub_result.setWordWrap(True)
        layout.addWidget(self.add_sub_result)
        
        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))
        layout.addWidget(back_btn)
        
        panel.setLayout(layout)
        return panel

    def toggle_decimal_input(self, digits_input):
        digits_input.setVisible(not digits_input.isVisible())

    # New calculation method for Add/Subtract
    def calculate_add_sub(self):
        try:
            # Get input values
            num1_str = self.num1_input.text()
            num2_str = self.num2_input.text()
            
            # Process decimal options for number 1
            d01 = 0
            if self.num1_decimal_cb.isChecked():
                if not self.num1_digits_input.text():
                    raise ValueError("Please enter decimal digits count for first number")
                d01 = int(self.num1_digits_input.text())
                if d01 <= 0:
                    raise ValueError("Decimal digits must be positive")
                if d01 >= len(num1_str):
                    raise ValueError("Decimal digits count cannot exceed number length")
            
            # Process decimal options for number 2
            d02 = 0
            if self.num2_decimal_cb.isChecked():
                if not self.num2_digits_input.text():
                    raise ValueError("Please enter decimal digits count for second number")
                d02 = int(self.num2_digits_input.text())
                if d02 <= 0:
                    raise ValueError("Decimal digits must be positive")
                if d02 >= len(num2_str):
                    raise ValueError("Decimal digits count cannot exceed number length")
            
            # Convert binary numbers to decimal with two's complement
            # Use signed=True for two's complement
            num1_dec = base_to_decimal(num1_str, 2, len(num1_str), d01, u=True)
            num2_dec = base_to_decimal(num2_str, 2, len(num2_str), d02, u=True)
            
            # Perform calculation based on selected operation
            if self.add_radio.isChecked():
                result_dec = num1_dec + num2_dec
                operation = "+"
            else:
                result_dec = num1_dec - num2_dec
                operation = "-"
            
            # Format result with 4 decimal places
            result_str = f"{result_dec:.4f}"
            
            # Display result
            self.add_sub_result.setText(
                f"Result: {num1_str} (d={d01}) {operation} {num2_str} (d={d02}) = {result_str}"
            )
            
        except ValueError as ve:
            self.add_sub_result.setText(f"Error: {str(ve)}")
        except Exception as e:
            self.add_sub_result.setText(f"Error: {str(e)}")

# === App Execution ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicConverterApp()
    window.show()
    sys.exit(app.exec_())