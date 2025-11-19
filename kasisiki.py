# kasiski_keylength.py
# Step 1: Find repeated substrings and their spacings.
# Step 2: Collect all spacings into one list.
# Step 3: For each candidate key length f, count how many spacings are multiples of f.

import os
from collections import defaultdict

MIN_LEN = 3          # minimum repeated substring length
MAX_LEN = 10         # maximum repeated substring length to search
MIN_KEY_LEN = 2      # candidate key length range start
MAX_KEY_LEN = 20     # candidate key length range end

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
    Returns: dict: substring -> list of start positions (0-based).
    """
    n = len(ciphertext)
    occurrences = defaultdict(list)

    for length in range(min_len, min(max_len, n) + 1):
        for i in range(0, n - length + 1):
            sub = ciphertext[i:i + length]
            occurrences[sub].append(i)

    # Keep only substrings that appear at least twice
    repeated = {
        sub: pos_list
        for sub, pos_list in occurrences.items()
        if len(pos_list) >= 2
    }
    return repeated

def compute_spacings(positions):
    """
    Given a list of start positions (0-based), compute spacings
    between consecutive occurrences:
    spacing = next_start - prev_start
    """
    positions = sorted(positions)
    spacings = []
    for i in range(len(positions) - 1):
        spacing = positions[i + 1] - positions[i]
        spacings.append(spacing)
    return spacings

def collect_all_spacings(repeated_dict):
    """
    From all repeated substrings, collect spacings into a single list D.
    Uses only consecutive spacings for each substring.
    Returns: list of spacings (integers).
    """
    all_spacings = []
    for sub, positions in repeated_dict.items():
        spacings = compute_spacings(positions)
        all_spacings.extend(spacings)
    return all_spacings

def factor_score(spacings, min_key_len=2, max_key_len=20):
    """
    For each candidate key length f in [min_key_len, max_key_len],
    count how many spacings are multiples of f.
    Returns: dict f -> count.
    """
    counts = {f: 0 for f in range(min_key_len, max_key_len + 1)}
    for d in spacings:
        if d <= 0:
            continue
        for f in range(min_key_len, max_key_len + 1):
            if d % f == 0:
                counts[f] += 1
    return counts

def main():
    print("=== Kasiski Examination: Key Length Estimator ===")
    ciphertext = load_ciphertext()
    print("Ciphertext length:", len(ciphertext))
    print(f"Searching repeated substrings of length {MIN_LEN} to {MAX_LEN}...")

    repeated = find_repeated_substrings(ciphertext, MIN_LEN, MAX_LEN)

    if not repeated:
        print("No repeated substrings of length >= 3 found.")
        return

    # Optional: show how many patterns we found
    print(f"Total different repeated substrings found: {len(repeated)}")

    # Step 1: collect all spacings
    all_spacings = collect_all_spacings(repeated)
    print("Number of spacing values collected:", len(all_spacings))
    if not all_spacings:
        print("No spacings to analyze.")
        return

    # Step 2: factor scoring for candidate key lengths
    print(f"Analyzing key length candidates from {MIN_KEY_LEN} to {MAX_KEY_LEN}...")
    counts = factor_score(all_spacings, MIN_KEY_LEN, MAX_KEY_LEN)

    # Sort candidates by score (descending), then by length (ascending)
    sorted_candidates = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    print("\nCandidate key length scores (higher is more likely):")
    print("Length\tScore")
    for f, c in sorted_candidates:
        print(f"{f}\t{c}")

    # Optionally highlight top few
    top_n = 5
    print(f"\nTop {top_n} candidates:")
    for f, c in sorted_candidates[:top_n]:
        print(f"  Length {f}: score {c}")

if __name__ == "__main__":
    main()
