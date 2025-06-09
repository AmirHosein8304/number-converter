def decimal_to_base(num, base):
    if decimal_num == 0:
        return "0"
    digits = []
    while num:
        digits.append(str(num % base))
        num //= base
    if decimal_num < 0:
        digits.append("-")
    return "".join(digits[::-1])

def base_to_decimal(num_str, base):
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

convert_between_bases(int(input('')))