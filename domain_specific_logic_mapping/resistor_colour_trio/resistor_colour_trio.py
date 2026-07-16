""" return the resistance of a transistor 
calculated from the colour coding """

def label(colour_list):
    """ returns the resistor resistance in ohms or kiloohms as relevant """
    
    colour_dict = {"black": 0, "brown": 1, "red": 2, 
                     "orange": 3, "yellow": 4, "green": 5,
                     "blue": 6, "violet": 7, "grey": 8, "white": 9}
    
    uom_list = {0: "ohms", 1: "kiloohms", 2: "megaohms", 3: "gigaohms"}

    # set the base number
    base_number = 0
    base_exponent = 0
    for index in range(1, -1, -1):
        digit = colour_dict[colour_list[index]]
        base_number += (digit * 10 ** base_exponent)
        base_exponent += 1

    # multiply the number by the power of 10 represented by the third colour
    lastcolour_exponent = colour_dict[colour_list[2]]
    uom_index = lastcolour_exponent // 3
    unit_of_measure = uom_list[uom_index]
    lastcolour_factor = lastcolour_exponent % 3

    final_number = base_number * 10 ** lastcolour_factor
    # fix final_number and bump uom
    if final_number >= 1000:
        final_number /= 1000
        unit_of_measure = uom_list[uom_index+1]

    print(f"DEBUG: base_number: {base_number}")
    print(f"DEBUG: lastcolour_exponent: {lastcolour_exponent}")
    print(f"DEBUG: unit_of_measure: {unit_of_measure}")
    print(f"DEBUG: lastcolour_factor: {lastcolour_factor}")
    print(f"DEBUG: final_number: {final_number}")

    return f"{int(final_number)} " + unit_of_measure

def main():
    label(["red", "black", "red"])

if __name__ == "__main__":
    main()