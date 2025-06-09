def decimal_to_base(num, base):
    """Converts a decimal number to a number in the specified base."""
    # Handle the case of 0 separately
    if num == 0:
        return "0"

    # Characters to use for digits, supporting up to base 36
    digits_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Handle negative numbers
    is_negative = num < 0
    if is_negative:
        num = -num  # Work with the positive version of the number

    result_digits = []
    while num > 0:
        # Use the map to get the correct character for bases > 10
        result_digits.append(digits_map[num % base])
        num //= base
    
    # Combine the digits and reverse them to get the correct order
    result_str = "".join(result_digits[::-1])

    # Prepend the negative sign if the original number was negative
    return "-" + result_str if is_negative else result_str

def base_to_decimal(num_str, base):
    """Converts a number string from a specified base to a decimal number."""
    num_str = str(num_str)
    if not num_str:
        return 0
    
    is_negative = num_str[0] == "-"
    if is_negative:
        num_str = num_str[1:]
        
    decimal = 0
    for digit in num_str:
        if '0' <= digit <= '9':
            value = int(digit)
        else:
            # Assumes A-Z for digits 10 and above
            value = ord(digit.upper()) - ord('A') + 10
        
        if value >= base:
            raise ValueError(f"Invalid digit {digit} for base {base}")
            
        decimal = decimal * base + value
        
    return -decimal if is_negative else decimal

def convert_between_bases(num_str, from_base, to_base):
    """Converts a number from one base to another."""
    decimal = base_to_decimal(num_str, from_base)
    return decimal_to_base(decimal, to_base)

def two_complement(num_decimal, k):
    """
    Calculates the k-bit two's complement of a decimal number.
    """
    if not isinstance(num_decimal, int):
        raise TypeError("num_decimal must be an integer.")
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer representing the number of bits.")

    # Calculate the range for a k-bit two's complement number
    min_val = -(2**(k-1))
    max_val = (2**(k-1)) - 1

    if not (min_val <= num_decimal <= max_val):
        raise ValueError(f"Number {num_decimal} is out of range for {k}-bit two's complement. "
                         f"Range: [{min_val}, {max_val}]")

    if num_decimal < 0:
        # For negative numbers, two's complement is 2^k - |num_decimal|
        result = 2**k + num_decimal
    else:
        # For positive numbers, it's just the number itself
        result = num_decimal

    # Convert the result to a binary string
    binary_representation = decimal_to_base(result, 2)
    
    # Pad with leading zeros to ensure it has k bits
    return binary_representation.zfill(k)

# Example usage and tests:

# Test decimal_to_base
print(f"Decimal 10 to base 2: {decimal_to_base(10, 2)}") # Expected: 1010
print(f"Decimal 16 to base 16: {decimal_to_base(16, 16)}") # Expected: 10
print(f"Decimal 255 to base 16: {decimal_to_base(255, 16)}") # Expected: FF
print(f"Decimal -10 to base 2: {decimal_to_base(-10, 2)}") # Expected: -1010
print(f"Decimal 0 to base 10: {decimal_to_base(0, 10)}") # Expected: 0

# Test base_to_decimal
print(f"Binary 1010 to decimal: {base_to_decimal('1010', 2)}") # Expected: 10
print(f"Hex 10 to decimal: {base_to_decimal('10', 16)}") # Expected: 16
print(f"Hex FF to decimal: {base_to_decimal('FF', 16)}") # Expected: 255
print(f"Binary -1010 to decimal: {base_to_decimal('-1010', 2)}") # Expected: -10
print(f"Empty string to decimal: {base_to_decimal('', 10)}") # Expected: 0

# Test convert_between_bases
print(f"Convert 1010 (base 2) to base 10: {convert_between_bases('1010', 2, 10)}") # Expected: 10
print(f"Convert FF (base 16) to base 2: {convert_between_bases('FF', 16, 2)}") # Expected: 11111111
print(f"Convert 10 (base 16) to base 10: {convert_between_bases('10', 16, 10)}") # Expected: 16

# Test two_complement
print(f"Two's complement of -6 with 4 bits: {two_complement(-6, 4)}") # Expected: 1010
print(f"Two's complement of 6 with 4 bits: {two_complement(6, 4)}")   # Expected: 0110
print(f"Two's complement of -1 with 4 bits: {two_complement(-1, 4)}") # Expected: 1111
print(f"Two's complement of 0 with 4 bits: {two_complement(0, 4)}")   # Expected: 0000
print(f"Two's complement of -8 with 4 bits: {two_complement(-8, 4)}") # Expected: 1000 (min value)
print(f"Two's complement of 7 with 4 bits: {two_complement(7, 4)}")   # Expected: 0111 (max value)

# Test error handling for two_complement
try:
    two_complement(-9, 4)
except ValueError as e:
    print(f"Error: {e}") # Expected: Number -9 is out of range for 4-bit two's complement. Range: [-8, 7]

try:
    two_complement(8, 4)
except ValueError as e:
    print(f"Error: {e}") # Expected: Number 8 is out of range for 4-bit two's complement. Range: [-8, 7]

try:
    two_complement(5, 0)
except ValueError as e:
    print(f"Error: {e}") # Expected: k must be a positive integer representing the number of bits.

try:
    two_complement(5, 4j)
except TypeError as e:
    print(f"Error: {e}") # Expected: num_decimal must be an integer.