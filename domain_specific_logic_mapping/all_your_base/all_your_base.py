""" Converts a number from one base to another """
import math

def rebase(input_base, digits, output_base):
    """ rebase """

    # Exceptions
    if input_base < 2:
        raise ValueError("input base must be >= 2")
    if output_base < 2:
        raise ValueError("output base must be >= 2")
    for index, digit in enumerate(digits):
        if not 0 <= digits[index] < input_base:
            raise ValueError("all digits must satisfy 0 <= d < input base")    

    # rebase to base_10    
    if digits == [] or not any(digits):
        return [0]
    
    base_10_number = 0
    for index, digit in enumerate(digits):
        base_10_number += int(digit) * input_base ** (len(digits)-index-1)

    # get the starting power exponent of out_base >= base_10_number
    ob_power: int = lowest_power_exponent(output_base, base_10_number)
    # print(f"DEBUG: ob_power: {ob_power}")
    if output_base ** ob_power > base_10_number:
        ob_power -= 1

    # rebase to output_base
    oblist = []
    remainder = base_10_number
    for index in range(ob_power, -1, -1):
        exponent = output_base ** index
        oblist.append(remainder // exponent)
        new_remainder = remainder % exponent
        remainder = new_remainder
        
        # print(f"DEBUG: index: {index}")
        # print(f"DEBUG: exponent: {exponent}")
        # print(f"remainder: {remainder}")
    
    return oblist

def lowest_power_exponent(base, target):
    return math.ceil(math.log(target, base))

def main():
    rebase(4, [3, 0, 1], 10)

if __name__ == "__main__":
    main()