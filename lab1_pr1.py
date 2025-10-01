# Alfabetul definit dupa tabel
ALFABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
L2N = {lit: i for i, lit in enumerate(ALFABET)}  # literă -> număr
N2L = {i: lit for i, lit in enumerate(ALFABET)}  # număr -> literă


def validate_text(text: str) -> bool:
    # Permitem DOAR litere din alfabetul latin A–Z
    for c in text:
        if not (c.isalpha() and c.upper() in ALFABET):
            return False
    return True


def clean_text(text: str) -> str:
    # Transformă în majuscule.
    return text.upper()


def caesar_encrypt(clar: str, k: int) -> str:
    rez = []
    for ch in clar:
        x = L2N[ch]          # reprezentare numerică (0..25)
        y = (x + k) % 26     # deplasare cu cheia
        rez.append(N2L[y])
    return "".join(rez)


def caesar_decrypt(cripto: str, k: int) -> str:
    rez = []
    for ch in cripto:
        y = L2N[ch]
        x = (y - k) % 26
        rez.append(N2L[x])
    return "".join(rez)


def read_key() -> int:
    # Citește până când avem un int între 1 și 25
    while True:
        s = input("Introdu cheia (1–25): ").strip()
        if s.isdigit():
            k = int(s)
            if 1 <= k <= 25:
                return k
        print("Eroare: cheia trebuie să fie un număr întreg între 1 și 25.")


def main():
    type_oper = input("Alege operația (criptare/decriptare): ").strip().lower()
    while type_oper != 'criptare' and type_oper != 'decriptare':
        type_oper = input("Operație invalidă! Folosește 'criptare' sau 'decriptare': ").strip().lower()

    text = input("Introdu textul (doar litere, fără spații): ").strip()
    while not validate_text(text):
        text = input("Eroare: sunt permise doar litere A–Z / a–z. Dă un nou text: ").strip()

    text = clean_text(text)
    k = read_key()

    if type_oper == "criptare":
        print("Criptograma:", caesar_encrypt(text, k))
    elif type_oper == "decriptare":
        print("Mesaj decriptat:", caesar_decrypt(text, k))


if __name__ == "__main__":
    main()
