import random

# ========================= PERMUTATION TABLES =========================

# P-box permutation table (used after S-boxes)
P_TABLE = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]


# ========================= UTILITY FUNCTIONS =========================


def format_binary(binary_str, group_size=4):
    """Format binary string with spaces for readability"""
    return ' '.join([binary_str[i:i + group_size] for i in range(0, len(binary_str), group_size)])


def xor_binary_strings(str1, str2):
    """XOR two binary strings of equal length"""
    if len(str1) != len(str2):
        raise ValueError("Binary strings must have equal length")

    result = ''.join(['0' if str1[i] == str2[i] else '1' for i in range(len(str1))])
    return result


# ========================= DES FUNCTIONS =========================

def permute(input_bits, table):
    """
    Apply permutation to input bits using the given table
    """
    output = ''
    for position in table:
        output += input_bits[position - 1]  # Convert to 0-indexed
    return output


def apply_p_permutation(sbox_output):
    """
    Apply P-box permutation to S-box output
    """
    if len(sbox_output) != 32:
        raise ValueError(f"S-box output must be 32 bits, got {len(sbox_output)}")

    return permute(sbox_output, P_TABLE)


def calculate_ri(l_prev, sbox_output):
    """
    Calculate Ri for round k given L(k-1) and S-box output
    """
    # Apply P permutation to S-box output
    p_output = apply_p_permutation(sbox_output)

    # XOR with L(k-1)
    ri = xor_binary_strings(l_prev, p_output)

    return ri, p_output


# ========================= DISPLAY FUNCTIONS =========================

def display_p_table():
    """Display the P permutation table"""
    print("\n" + "=" * 70)
    print("P-BOX PERMUTATION TABLE")
    print("=" * 70)
    print("\nThe P-box permutes 32 bits from S-box output:")
    print("\nTable (positions are 1-indexed):")

    for i in range(0, len(P_TABLE), 8):
        row = P_TABLE[i:i + 8]
        print("  " + "  ".join([f"{val:2d}" for val in row]))


def display_calculation_steps(round_num, l_prev, sbox_output, p_output, ri):
    """Display all calculation steps"""
    print("\n" + "=" * 70)
    print(f"CALCULATION STEPS FOR ROUND {round_num}")
    print("=" * 70)

    print(f"\nSTEP 1: Input Data")
    print(f"  L(k-1) = {format_binary(l_prev)}")

    print(f"\n  S-box output = {format_binary(sbox_output)}")

    print(f"\nSTEP 2: Apply P Permutation")
    print(f"  Before P: {format_binary(sbox_output)}")
    print(f"  After P:  {format_binary(p_output)}")


    print(f"\nSTEP 3: XOR with L(k-1)")
    print(f"  L(k-1)      = {format_binary(l_prev)}")
    print(f"  P(S-output) = {format_binary(p_output)}")
    print(f"  ──────────────────────────────────── (XOR)")
    print(f"  Ri          = {format_binary(ri)}")

    print("\n" + "=" * 70)
    print(f"RESULT: R{round_num} = {format_binary(ri)}")
    print("=" * 70)


def display_detailed_p_permutation(sbox_output, p_output):
    """Display detailed P permutation mapping"""
    print("\n" + "=" * 70)
    print("DETAILED P PERMUTATION MAPPING")
    print("=" * 70)

    print("\nInput (S-box output):")
    for i in range(0, 32, 8):
        bits = sbox_output[i:i + 8]
        positions = f"[{i + 1:2d}-{i + 8:2d}]"
        print(f"  Bits {positions}: {' '.join(bits)}")

    print("\nOutput (After P permutation):")
    for i in range(0, 32, 8):
        bits = p_output[i:i + 8]
        positions = f"[{i + 1:2d}-{i + 8:2d}]"
        sources = P_TABLE[i:i + 8]
        print(f"  Bits {positions}: {' '.join(bits)}  (from positions {sources})")

    print("=" * 70)


# ========================= INPUT FUNCTIONS =========================

def get_user_input():
    """Get input from user"""
    print("\n" + "=" * 70)
    print("INPUT DATA")
    print("=" * 70)

    while True:
        print("\nChoose input method:")
        print("  1. Enter binary values")
        print("  2. Generate random values")
        choice = input("\nYour choice (1/2): ").strip()

        if choice == '1':
            return get_binary_input()
        elif choice == '2':
            return generate_random_input()

        else:
            print("Invalid choice. Please enter 1, 2.")


def get_binary_input():
    """Get binary input from user"""
    print("\nEnter binary values (32 bits, spaces optional):")

    while True:
        round_num = input("\n  Round number k: ").strip()
        try:
            round_num = int(round_num)
            if 1 <= round_num <= 16:
                break
            print("  Round number must be between 1 and 16")
        except ValueError:
            print("  Please enter a valid number")

    while True:
        l_prev = input(f"  L(k-1) (binary): ").strip().replace(" ", "")
        if len(l_prev) == 32 and all(c in '01' for c in l_prev):
            break
        print("  Please enter exactly 32 binary digits (0 or 1)")

    while True:
        sbox_output = input(f"  S-box output (binary): ").strip().replace(" ", "")
        if len(sbox_output) == 32 and all(c in '01' for c in sbox_output):
            break
        print("  Please enter exactly 32 binary digits (0 or 1)")

    return round_num, l_prev, sbox_output


def generate_random_input():
    """Generate random input values"""
    print("\nGenerating random values...")

    round_num = random.randint(1, 16)
    l_prev = ''.join([str(random.randint(0, 1)) for _ in range(32)])
    sbox_output = ''.join([str(random.randint(0, 1)) for _ in range(32)])

    print(f"\n  Round number k: {round_num}")
    print(f"  L(k-1): {format_binary(l_prev)} ")
    print(f"  S-box output: {format_binary(sbox_output)} ")

    return round_num, l_prev, sbox_output


# ========================= MAIN PROGRAM =========================

def main():
    """Main program"""
    print("=" * 70)
    print("DES ALGORITHM - ROUND CALCULATION")
    print("Task 2.8: Calculate Ri for round k")
    print("=" * 70)

    print("\nFormula:")
    print("  Ri = L(k-1) ⊕ f(R(k-1), Ki)")
    print("     = L(k-1) ⊕ P(S-box output)")

    # Display P-box table
    display_p_table()

    # Get input
    round_num, l_prev, sbox_output = get_user_input()

    # Calculate Ri
    ri, p_output = calculate_ri(l_prev, sbox_output)

    # Display results
    display_calculation_steps(round_num, l_prev, sbox_output, p_output, ri)

    # Display detailed permutation mapping
    print("\nWould you like to see detailed P permutation mapping? (y/n): ", end="")
    if input().strip().lower() == 'y':
        display_detailed_p_permutation(sbox_output, p_output)

    # Ask if user wants to continue
    print("\n" + "=" * 70)
    print("Would you like to perform another calculation? (y/n): ", end="")
    if input().strip().lower() == 'y':
        print("\n" * 2)
        main()
    else:
        print("\nThank you for using the DES Round Calculator!")
        print("=" * 70)


if __name__ == "__main__":
    main()