# vigenere_trykey.py
# Minimal version: load ciphertext from cipher.txt, input key, decrypt using Vigenère.

def text_to_numbers(text: str):
    """Convert letters A–Z to 0–25."""
    text = text.upper()
    return [ord(ch) - ord('A') for ch in text]

def numbers_to_text(nums):
    """Convert 0–25 numbers back to letters."""
    return "".join(chr(n + ord('A')) for n in nums)

def decrypt_vigenere(ciphertext: str, key: str) -> str:
    """Vigenère decryption: P = (C - K) mod 26."""
    key = key.upper()

    if not key.isalpha():
        raise ValueError("Key must contain letters only.")

    ct = text_to_numbers(ciphertext)
    k = text_to_numbers(key)
    L = len(k)

    pt = [(ct[i] - k[i % L]) % 26 for i in range(len(ct))]
    return numbers_to_text(pt)

def load_ciphertext():
    """Load ciphertext strictly from cipher.txt."""
    with open("cipher.txt", "r", encoding="utf-8") as f:
        text = f.read().strip().replace(" ", "").replace("\n", "")
        if not text.isalpha():
            raise ValueError("cipher.txt: letters only.")
        return text.upper()

def main():
    ciphertext = load_ciphertext()
    print(f"Ciphertext loaded ({len(ciphertext)} letters).")

    key = input("Enter key: ").strip()
    plaintext = decrypt_vigenere(ciphertext, key)

    print("\nDecrypted plaintext:\n")
    print(plaintext)

if __name__ == "__main__":
    main()
