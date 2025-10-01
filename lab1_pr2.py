from lab1_pr1 import ALFABET, validate_text, clean_text, read_key


def validate_k2(k2: str) -> bool:
    # doar litere A–Z/a–z, lungime >= 7
    if not isinstance(k2, str) or len(k2) < 7:
        return False
    for ch in k2:
        if not (ch.isalpha() and ch.upper() in ALFABET):
            return False
    return True


def build_perm_from_k2(k2: str):
    # Literele unice din k2 (în ordinea apariției), apoi restul din ALFABET
    k2u = k2.upper()
    seen = set()
    perm = []
    for ch in k2u:
        if ch in ALFABET and ch not in seen:
            seen.add(ch)
            perm.append(ch)
    for ch in ALFABET:
        if ch not in seen:
            perm.append(ch)
    L2N = {lit: i for i, lit in enumerate(perm)}
    N2L = {i: lit for i, lit in enumerate(perm)}
    return perm, L2N, N2L


def caesar2_encrypt(clar: str, k1: int, k2: str) -> str:
    _, L2N, N2L = build_perm_from_k2(k2)
    text = clean_text(clar)
    rez = []
    for ch in text:
        x = L2N[ch]
        y = (x + k1) % 26
        rez.append(N2L[y])
    return "".join(rez)


def caesar2_decrypt(cripto: str, k1: int, k2: str) -> str:
    _, L2N, N2L = build_perm_from_k2(k2)
    text = clean_text(cripto)
    rez = []
    for ch in text:
        y = L2N[ch]
        x = (y - k1) % 26
        rez.append(N2L[x])
    return "".join(rez)


def read_key2() -> str:
    while True:
        s = input("Introdu cheia 2 (doar litere, lungime ≥ 7): ").strip()
        if validate_k2(s):
            return s
        print("Eroare: cheia 2 trebuie să aibă cel puțin 7 litere A–Z / a–z.")


def main():
    op = input("Alege operația (criptare/decriptare): ").strip().lower()
    while op != 'criptare' and op != 'decriptare':
        op = input("Operație invalidă! Folosește 'criptare' sau 'decriptare': ").strip().lower()

    text = input("Introdu textul (doar litere, fără spații): ").strip()
    while not validate_text(text):
        text = input("Eroare: sunt permise doar litere A–Z / a–z. Dă un nou text: ").strip()

    k1 = read_key()     # 1..25 (din baza ta)
    k2 = read_key2()    # doar litere, lungime ≥ 7

    if op == "criptare":
        print("Criptograma:", caesar2_encrypt(text, k1, k2))
    else:
        print("Mesaj decriptat:", caesar2_decrypt(text, k1, k2))


if __name__ == "__main__":
    main()
