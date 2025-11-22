# ioc_check.py
# Minimal IC-based key length checker (fixed range 2..20, ciphertext from cipher.txt)

from collections import Counter

MIN_KEY = 2
MAX_KEY = 20


def load_ciphertext(path="cipher.txt"):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip().replace(" ", "").replace("\n", "")
    if not text.isalpha():
        raise ValueError("cipher.txt: letters only.")
    return text.upper()


def index_of_coincidence(text: str) -> float:
    N = len(text)
    if N <= 1:
        return 0.0
    counter = Counter(text)
    numerator = sum(n * (n - 1) for n in counter.values())
    return numerator / (N * (N - 1))


def split_by_key_length(ciphertext: str, key_len: int):
    groups = ['' for _ in range(key_len)]
    for i, ch in enumerate(ciphertext):
        groups[i % key_len] += ch
    return groups


def analyze_key_lengths(ciphertext: str, min_len=MIN_KEY, max_len=MAX_KEY):
    results = {}
    for k in range(min_len, max_len + 1):
        groups = split_by_key_length(ciphertext, k)
        group_ics = [index_of_coincidence(g) for g in groups if len(g) > 1]
        avg_ic = sum(group_ics) / len(group_ics) if group_ics else 0.0
        results[k] = avg_ic
    return results


def main():
    ciphertext = load_ciphertext()
    overall_ic = index_of_coincidence(ciphertext)

    print(f"Overall IC: {overall_ic:.4f}")
    print("Reference: random≈0.038, English≈0.066")

    results = analyze_key_lengths(ciphertext)

    print("\nKey length IC scores (2~20):")
    print("Len\tAvg_IC")
    for k in range(MIN_KEY, MAX_KEY + 1):
        print(f"{k}\t{results[k]:.4f}")

    sorted_candidates = sorted(results.items(), key=lambda x: -x[1])
    print("\nTop candidates:")
    for k, ic in sorted_candidates[:5]:
        print(f"  {k}: {ic:.4f}")


if __name__ == "__main__":
    main()
