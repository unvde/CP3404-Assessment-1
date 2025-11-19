# ioc_check.py
# Purpose: Use Index of Coincidence (IC) to validate candidate key lengths
# for a Vigenère cipher.

import os
from collections import Counter

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

def index_of_coincidence(text: str) -> float:
    """
    Compute the Index of Coincidence (IC) for a given text.

    IC = sum_i (n_i * (n_i - 1)) / (N * (N - 1))
    where n_i is the count of letter i, and N is total length.
    """
    N = len(text)
    if N <= 1:
        return 0.0
    counter = Counter(text)
    numerator = sum(n * (n - 1) for n in counter.values())
    denominator = N * (N - 1)
    return numerator / denominator

def split_by_key_length(ciphertext: str, key_len: int):
    """
    Split ciphertext into key_len groups by position modulo key_len.
    groups[j] contains characters with indices i where i % key_len == j.
    """
    groups = ['' for _ in range(key_len)]
    for i, ch in enumerate(ciphertext):
        groups[i % key_len] += ch
    return groups

def analyze_key_lengths(ciphertext: str, min_len: int, max_len: int):
    """
    For each candidate key length in [min_len, max_len],
    split ciphertext into groups and compute average IC.
    Returns: dict key_len -> (average_IC, list_of_group_ICs)
    """
    results = {}
    for k in range(min_len, max_len + 1):
        groups = split_by_key_length(ciphertext, k)
        group_ics = [index_of_coincidence(g) for g in groups if len(g) > 1]
        if not group_ics:
            avg_ic = 0.0
        else:
            avg_ic = sum(group_ics) / len(group_ics)
        results[k] = (avg_ic, group_ics)
    return results

def main():
    print("=== Index of Coincidence (IC) Key Length Checker ===")
    ciphertext = load_ciphertext()
    print("Ciphertext length:", len(ciphertext))

    # Overall IC of the ciphertext
    overall_ic = index_of_coincidence(ciphertext)
    print(f"\nOverall IC of ciphertext: {overall_ic:.4f}")
    print("For reference: random text ≈ 0.038, English ≈ 0.066")

    # Ask user for key length range
    try:
        min_len = int(input("\nEnter minimum key length to test (e.g. 2): ").strip())
        max_len = int(input("Enter maximum key length to test (e.g. 20): ").strip())
    except ValueError:
        print("Invalid input. Please enter integers for key length range.")
        return

    if min_len < 1 or max_len < min_len:
        print("Invalid range.")
        return

    results = analyze_key_lengths(ciphertext, min_len, max_len)

    print("\nCandidate key length IC scores:")
    print("Len\tAvg_IC")
    for k in range(min_len, max_len + 1):
        avg_ic, _ = results[k]
        print(f"{k}\t{avg_ic:.4f}")

    # Show top few candidates sorted by Avg_IC (descending)
    sorted_candidates = sorted(results.items(), key=lambda x: -x[1][0])
    top_n = min(5, len(sorted_candidates))
    print(f"\nTop {top_n} candidates by average IC:")
    for k, (avg_ic, group_ics) in sorted_candidates[:top_n]:
        print(f"  Key length {k}: Avg_IC = {avg_ic:.4f}")

if __name__ == "__main__":
    main()
