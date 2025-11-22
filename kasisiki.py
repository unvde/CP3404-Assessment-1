# kasiski.py
# Minimal merged version:
# 1) Find repeated substrings (len 3..10) and their spacings
# 2) Score candidate key lengths by multiples of spacings
# Ciphertext source: cipher.txt only

from collections import defaultdict

MIN_LEN = 3
MAX_LEN = 10
MIN_KEY_LEN = 2
MAX_KEY_LEN = 20


def load_ciphertext(path="cipher.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip().replace(" ", "").replace("\n", "")
    if not text.isalpha():
        raise ValueError("cipher.txt: letters only (A–Z).")
    return text.upper()


def find_repeated_substrings(ciphertext: str, min_len=MIN_LEN, max_len=MAX_LEN):
    """
    Return dict: substring -> sorted list of start positions (0-based),
    keeping only substrings that appear >= 2 times.
    """
    n = len(ciphertext)
    occ = defaultdict(list)

    for L in range(min_len, min(max_len, n) + 1):
        for i in range(n - L + 1):
            occ[ciphertext[i:i + L]].append(i)

    return {sub: sorted(pos) for sub, pos in occ.items() if len(pos) >= 2}


def spacings_from_positions(positions):
    """Given sorted positions, return consecutive spacings."""
    return [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]


def collect_all_spacings(repeated_dict):
    all_sp = []
    for positions in repeated_dict.values():
        all_sp.extend(spacings_from_positions(positions))
    return all_sp


def factor_score(spacings, min_key_len=MIN_KEY_LEN, max_key_len=MAX_KEY_LEN):
    counts = {f: 0 for f in range(min_key_len, max_key_len + 1)}
    for d in spacings:
        for f in counts:
            if d % f == 0:
                counts[f] += 1
    return counts


def main():
    ciphertext = load_ciphertext()
    repeated = find_repeated_substrings(ciphertext)

    if not repeated:
        print("No repeated substrings (len >= 3).")
        return

    # ---- Part A: print repeated substrings + spacings ----
    items = sorted(repeated.items(), key=lambda x: (len(x[0]), x[0]))
    for sub, pos in items:
        sp = spacings_from_positions(pos)
        pos_1 = [p + 1 for p in pos]  # human-readable
        print("-" * 40)
        print(f"Substring: {sub}")
        print(f"Length: {len(sub)}")
        print(f"Occurrences: {len(pos)}")
        print(f"Start positions (1-based): {pos_1}")
        print(f"Spacings: {sp}")

    print("-" * 40)
    print("Total different repeated substrings:", len(repeated))

    # ---- Part B: key length scoring ----
    all_spacings = collect_all_spacings(repeated)
    if not all_spacings:
        print("No spacings collected.")
        return

    counts = factor_score(all_spacings)
    sorted_candidates = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    print("\nCandidate key length scores:")
    print("Length\tScore")
    for f, c in sorted_candidates:
        print(f"{f}\t{c}")


if __name__ == "__main__":
    main()
