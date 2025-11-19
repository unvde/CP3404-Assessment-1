# kasiski_spacings.py
# Purpose: Find repeated substrings (length >= 3) in a ciphertext
# and compute spacings between the first letters of consecutive occurrences.

import os
from collections import defaultdict

MIN_LEN = 3      # minimum substring length to consider
MAX_LEN = 10     # max length to consider (can be increased, but grows fast)

def load_ciphertext():
    """
    Load ciphertext from cipher.txt if it exists.
    Otherwise, ask the user to input it.
    """
    if os.path.exists("cipher.txt"):
        with open("cipher.txt", "r", encoding="utf-8") as f:
            content = f.read().strip().replace(" ", "").replace("\n", "")
        if not content.isalpha():
            raise ValueError("cipher.txt must contain letters only (A–Z).")
        ciphertext = content.upper()
        print(f"Ciphertext loaded from cipher.txt ({len(ciphertext)} letters).")
    else:
        ciphertext = input("Enter ciphertext (letters only): ").strip().upper()
        if not ciphertext.isalpha():
            raise ValueError("Ciphertext must contain letters only (A–Z).")
    return ciphertext

def find_repeated_substrings(ciphertext: str, min_len=3, max_len=10):
    """
    Find all repeated substrings of length between min_len and max_len.
    Returns a dict: substring -> list of start positions (0-based).
    """
    n = len(ciphertext)
    occurrences = defaultdict(list)

    for length in range(min_len, min(max_len, n) + 1):
        for i in range(0, n - length + 1):
            sub = ciphertext[i:i + length]
            occurrences[sub].append(i)

    # Keep only substrings that appear at least twice
    repeated = {sub: pos_list for sub, pos_list in occurrences.items()
                if len(pos_list) >= 2}
    return repeated

def compute_spacings(positions):
    """
    Given a sorted list of start positions (0-based),
    compute spacings between consecutive occurrences.
    Spacing = next_start - prev_start.
    """
    positions = sorted(positions)
    spacings = []
    for i in range(len(positions) - 1):
        spacing = positions[i + 1] - positions[i]
        spacings.append(spacing)
    return spacings

def main():
    print("=== Repeated Substring Finder (Kasiski-style) ===")
    ciphertext = load_ciphertext()
    print("Ciphertext length:", len(ciphertext))
    print(f"Searching for repeated substrings of length {MIN_LEN} to {MAX_LEN}...")

    repeated = find_repeated_substrings(ciphertext, MIN_LEN, MAX_LEN)

    if not repeated:
        print("No repeated substrings of length >= 3 found.")
        return

    # Sort results for nicer output:
    #   first by substring length, then alphabetically
    items = sorted(repeated.items(), key=lambda x: (len(x[0]), x[0]))

    total_patterns = 0
    for sub, positions in items:
        total_patterns += 1
        # Convert to 1-based positions for human readability
        positions_1_based = [p + 1 for p in sorted(positions)]
        spacings = compute_spacings(positions)

        print("-" * 40)
        print(f"Substring: {sub}")
        print(f"Length: {len(sub)}")
        print(f"Occurrences: {len(positions)}")
        print(f"Start positions (1-based): {positions_1_based}")
        if spacings:
            print(f"Spacings between consecutive starts: {spacings}")
        else:
            print("Spacings: (only one occurrence, should not happen here)")

    print("-" * 40)
    print("Total different repeated substrings found:", total_patterns)

if __name__ == "__main__":
    main()
