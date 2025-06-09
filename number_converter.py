def decimal_to_base(num, base):
    num = abs(num)
    if num == 0:
        return "0"
    digits = []
    while num:
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
    
print(two_complement(decimal_to_base(-6,2),4))