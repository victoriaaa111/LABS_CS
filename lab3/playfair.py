def create_matrix(key):
    # Creates a 5x6 matrix for Romanian alphabet (30 letters, Î replaced with I)
    alfabet = "AĂÂBCDEFGHIJKLMNOPQRSȘTȚUVWXYZ"

    # remove duplicates, spaces from key and convert to uppercase
    key = key.upper().replace(" ", "")
    final_key = ""
    for c in key:
        if c not in final_key and c in alfabet:
            final_key += c

    # create string for matrix: key + rest of alphabet (without Î)
    string_matrix = final_key
    for letter in alfabet:
        if letter not in string_matrix and letter != 'Î':
            string_matrix += letter

    # create 5x6 matrix (30 positions for 30 letters, Î replaced with I)
    matrix_playfair = []
    for i in range(5):
        r = []
        for j in range(6):
            idx = i * 6 + j
            if idx < len(string_matrix):
                r.append(string_matrix[idx])
            else:
                r.append('')  # empty cells
        matrix_playfair.append(r)

    return matrix_playfair


def find_position(matrix, letter):
    # finds the position of a letter in the matrix
    if letter == 'Î':
        letter = 'I'

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == letter:
                return i, j
    return None, None


def show_matrix(matrix):
    # displays the encryption matrix
    print("\nEncryption matrix:")
    print("-" * 25)
    for r in matrix:
        print(" ".join([f"{c:2}" if c else "  " for c in r]))
    print("-" * 25)


def prepare_text(text, encryption=True):
    # prepares the text for encryption/decryption
    # convert to uppercase and remove spaces
    text = text.upper().replace(" ", "")

    # replace Î with I
    text = text.replace('Î', 'I')

    if encryption:
        # split into pairs and insert X between double letters
        text_processed = ""
        i = 0
        while i < len(text):
            text_processed += text[i]

            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    text_processed += 'X'
                else:
                    text_processed += text[i + 1]
                    i += 1
            i += 1

        # add X at the end if we have odd number of letters
        if len(text_processed) % 2 != 0:
            text_processed += 'X'

        return text_processed
    else:
        # for decryption, just return text without spaces
        return text


def encrypt_pair(matrix, l1, l2):
    # encrypts a pair of letters according to Playfair rules
    r1, c1 = find_position(matrix, l1)
    r2, c2 = find_position(matrix, l2)

    if r1 is None or r2 is None:
        return l1 + l2  # return unchanged if not found in matrix

    # Case 1: Same row
    if r1 == r2:
        return matrix[r1][(c1 + 1) % 6] + matrix[r2][(c2 + 1) % 6]

    # Case 2: Same column
    elif c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]

    # Case 3: different rows and columns
    else:
        return matrix[r1][c2] + matrix[r2][c1]


def decrypt_pair(matrix, l1, l2):
    # decrypts a pair of letters according to Playfair rules
    r1, c1 = find_position(matrix, l1)
    r2, c2 = find_position(matrix, l2)

    if r1 is None or r2 is None:
        return l1 + l2

    # Case 1: Same row (move left)
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 6] + matrix[r2][(c2 - 1) % 6]

    # Case 2: Same column (move up)
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]

    # Case 3: Rectangle (same as encryption)
    else:
        return matrix[r1][c2] + matrix[r2][c1]


def encrypt_playfair(text, key):
    # Encrypts text using Playfair cipher
    matrix = create_matrix(key)
    processed_text = prepare_text(text, encryption=True)

    cipher = ""
    for i in range(0, len(processed_text), 2):
        if i + 1 < len(processed_text):
            cipher += encrypt_pair(matrix, processed_text[i], processed_text[i + 1])

    return cipher, matrix


def decrypt_playfair(cipher, key):
    # Decrypts ciphertext using Playfair cipher
    matrix = create_matrix(key)
    processed_text = prepare_text(cipher, encryption=False)

    message = ""
    for i in range(0, len(processed_text), 2):
        if i + 1 < len(processed_text):
            message += decrypt_pair(matrix, processed_text[i], processed_text[i + 1])

    return message, matrix


def validate_input(text):
    # validates that text contains only letters and spaces
    allowed_char = "AĂÂBCDEFGHIÎJKLMNOPQRSȘȚTUVWXYZaăâbcdefghiîjklmnopqrsșțtuvwxyz "
    for c in text:
        if c not in allowed_char:
            return False
    return True


def main():
    print("=" * 60)
    print("PLAYFAIR CIPHER FOR ROMANIAN LANGUAGE (31 LETTERS, Î REPLACED WITH I)")
    print("=" * 60)

    while True:
        print("\nChoose operation:")
        print("1 - Encryption")
        print("2 - Decryption")
        print("3 - Exit")

        option = input("\nYour choice (1/2/3): ").strip()

        if option == '3':
            print("Goodbye!")
            break

        if option not in ['1', '2']:
            print("Invalid option! Choose 1, 2 or 3.")
            continue

        # Read key
        while True:
            key= input("\nEnter key (minimum 7 characters): ").strip()

            if not validate_input(key):
                print("ERROR: Key can only contain letters (A-Z, a-z, Ă, Â, Î, Ș, Ț) and spaces!")
                print("Valid range: A-Z, a-z, Ă, Â, Î, Ș, Ț and spaces")
                continue

            key_no_spaces = key.replace(" ", "")
            if len(key_no_spaces) < 7:
                print(f"ERROR: Key must have minimum 7 characters! (you have {len(key_no_spaces)})")
                continue

            break

        # Encryption
        if option == '1':
            while True:
                message = input("\nEnter message to encrypt: ").strip()

                if not validate_input(message):
                    print("ERROR: Message can only contain letters (A-Z, a-z, Ă, Â, Î, Ș, Ț) and spaces!")
                    print("Valid range: A-Z, a-z, Ă, Â, Î, Ș, Ț and spaces")
                    continue

                break

            cipher, matrix = encrypt_playfair(message, key)

            show_matrix(matrix)
            print(f"\nOriginal message: {message}")
            print(f"Processed message: {prepare_text(message, True)}")
            print(f"\n{'=' * 60}")
            print(f"CIPHERTEXT: {cipher}")
            print(f"{'=' * 60}")

        # Decryption
        else:
            while True:
                cipher = input("\nEnter ciphertext to decrypt: ").strip()

                if not validate_input(cipher):
                    print("ERROR: Ciphertext can only contain letters (A-Z, a-z, Ă, Â, Î, Ș, Ț) and spaces!")
                    print("Valid range: A-Z, a-z, Ă, Â, Î, Ș, Ț and spaces")
                    continue

                break

            message, matrix = decrypt_playfair(cipher, key)

            show_matrix(matrix)
            print(f"\nCiphertext: {cipher}")
            print(f"\n{'=' * 60}")
            print(f"DECRYPTED MESSAGE: {message}")
            print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
