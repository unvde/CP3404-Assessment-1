# vigenere_trykey.py
# Purpose: Try a guessed key to decrypt a ciphertext encrypted with Vigenère cipher.
# Language: English only version

import os

def text_to_numbers(text: str):
    """Convert letters to 0–25 numbers."""
    text = text.upper()
    nums = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            nums.append(ord(ch) - ord('A'))
        else:
            raise ValueError(f"Non-letter character detected: {ch!r}")
    return nums

def numbers_to_text(nums):
    """Convert 0–25 numbers back to letters."""
    return "".join(chr(n + ord('A')) for n in nums)

def decrypt_vigenere(ciphertext: str, key: str) -> str:
    """
    Vigenère decryption:
    C = (P + K) mod 26
    => P = (C - K) mod 26
    The key is repeated cyclically until ciphertext ends.
    """
    if not key.isalpha():
        raise ValueError("Key must contain letters only (A–Z or a–z).")

    ct_nums = text_to_numbers(ciphertext)
    key_nums = text_to_numbers(key)
    key_len = len(key_nums)

    pt_nums = []
    for i, c in enumerate(ct_nums):
        k = key_nums[i % key_len]
        p = (c - k) % 26
        pt_nums.append(p)

    return numbers_to_text(pt_nums)

def load_ciphertext():
    """Try to load ciphertext from cipher.txt if it exists."""
    if os.path.exists("cipher.txt"):
        with open("cipher.txt", "r", encoding="utf-8") as f:
            content = f.read().strip().replace(" ", "").replace("\n", "")
            if not content.isalpha():
                raise ValueError("cipher.txt must contain letters only (A–Z).")
            print(f"Ciphertext loaded from cipher.txt ({len(content)} letters).")
            return content
    print("No cipher.txt found, using default ciphertext.")
    return DEFAULT_CIPHERTEXT

def main():
    print("=== Vigenère Cipher Key Tester ===")
    ciphertext = load_ciphertext()
    print("Current ciphertext:", ciphertext)
    user_input = input("Use this ciphertext (d) or enter your own (o)? [d/o]: ").strip().lower()

    if user_input == 'o':
        ciphertext = input("Enter ciphertext (letters only): ").strip()

    key = input("Enter your guessed key (letters only): ").strip()

    try:
        plaintext = decrypt_vigenere(ciphertext, key)
    except ValueError as e:
        print("Error:", e)
        return

    print("--------------")
    print("Decrypted (candidate plaintext):", plaintext)
    print("--------------")

if __name__ == "__main__":
    main()
