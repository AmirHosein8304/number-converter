def decimal_to_base(num, base):
    """Converts a decimal number to a number in the specified base."""
    if not isinstance(num, int):
        raise TypeError("Input number must be an integer.")
    
    # Handle the case of 0
    if num == 0:
        return "0"

    # Handle negative numbers by converting the positive part and adding a '-' sign
    if num < 0:
        return "-" + decimal_to_base(abs(num), base)

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if base > len(digits):
        raise ValueError(f"Bases greater than {len(digits)} are not supported.")

    result = []
    while num > 0:
        remainder = num % base
        result.append(digits[remainder])
        num //= base
    
    # The digits are generated in reverse order, so we reverse them back
    return "".join(result[::-1])

def base_to_decimal(num_str, base):
    """Converts a number string from a specified base to a decimal number."""
    if not isinstance(num_str, str):
        raise TypeError("Input number must be a string.")
        
    if not num_str:
        return 0

    # Check for a negative sign
    is_negative = num_str[0] == "-"
    if is_negative:
        num_str = num_str[1:]

    decimal_value = 0
    power = 0
    
    # Iterate through the string in reverse to calculate decimal value
    for digit in reversed(num_str):
        value = 0
        if '0' <= digit <= '9':
            value = int(digit)
        elif 'A' <= digit.upper() <= 'Z':
            value = ord(digit.upper()) - ord('A') + 10
        else:
            raise ValueError(f"Invalid character '{digit}' in number string.")

        if value >= base:
            raise ValueError(f"Invalid digit '{digit}' for base {base}.")
        
        decimal_value += value * (base ** power)
        power += 1

    return -decimal_value if is_negative else decimal_value

def convert_between_bases(num_str, from_base, to_base):
    """
    Converts a number string from a given base to another given base.
    This is done by first converting to decimal (base 10) as an intermediate step.
    """
    try:
        # Convert the source number (from_base) to its decimal equivalent
        decimal_value = base_to_decimal(num_str, from_base)
        
        # Convert the decimal value to the target base (to_base)
        return decimal_to_base(decimal_value, to_base)
    except (ValueError, TypeError) as e:
        # Pass the error message up to the caller
        return str(e)

# Main execution block to run the converter from the command line
if __name__ == "__main__":
    print("--- Number Base Converter ---")
    print("Converts a number from one base to another (supports bases 2-36).")
    
    try:
        num_str_input = input("Enter the number string: ")
        from_base_input = int(input("Enter the base of this number (e.g., 2, 8, 10, 16): "))
        to_base_input = int(input("Enter the target base to convert to: "))

        # Perform the conversion
        result = convert_between_bases(num_str_input, from_base_input, to_base_input)

        # Print the result
        print("\n--- Result ---")
        print(f"'{num_str_input}' in base {from_base_input} is '{result}' in base {to_base_input}.")

    except ValueError:
        # Catches errors from int() conversion if input is not a number
        print("\nError: Please enter valid integers for the bases.")
    except Exception as e:
        # Catches any other unexpected errors
        print(f"\nAn unexpected error occurred: {e}")

