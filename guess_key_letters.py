# guess_key_letters.py
# Minimal key-letter guesser:
# 1) load ciphertext from cipher.txt
# 2) input key length
# 3) split into Caesar groups
# 4) for each group, find most likely shift by chi-squared vs English frequencies
# 5) output most likely key letters

from collections import Counter

# English letter frequencies (A-Z), normalized
EN_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]


def load_ciphertext(path="cipher.txt"):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip().replace(" ", "").replace("\n", "")
    if not text.isalpha():
        raise ValueError("cipher.txt: letters only.")
    return text.upper()


def text_to_nums(text: str):
    return [ord(ch) - ord('A') for ch in text]


def nums_to_text(nums):
    return "".join(chr(n + ord('A')) for n in nums)


def split_by_key_length(ciphertext: str, key_len: int):
    groups = [[] for _ in range(key_len)]
    nums = text_to_nums(ciphertext)
    for i, n in enumerate(nums):
        groups[i % key_len].append(n)
    return groups


def caesar_decrypt_nums(group_nums, shift):
    # shift = key letter (0=A,1=B...) used in Vigenère
    return [(c - shift) % 26 for c in group_nums]


def chi_squared_score(plain_nums):
    N = len(plain_nums)
    if N == 0:
        return float("inf")

    counts = Counter(plain_nums)
    score = 0.0
    for i in range(26):
        observed = counts.get(i, 0)
        expected = EN_FREQ[i] * N
        if expected > 0:
            score += (observed - expected) ** 2 / expected
    return score


def best_shifts_for_group(group_nums, top_n=3):
    scored = []
    for shift in range(26):
        plain = caesar_decrypt_nums(group_nums, shift)
        scored.append((shift, chi_squared_score(plain)))

    scored.sort(key=lambda x: x[1])  # lower chi^2 = better
    return scored[:top_n]


def main():
    ciphertext = load_ciphertext()
    key_len = int(input("Enter key length: ").strip())
    if key_len < 1:
        raise ValueError("Key length must be >= 1.")

    groups = split_by_key_length(ciphertext, key_len)

    best_key_nums = []
    print("\nMost likely key letters by position:")
    for idx, g in enumerate(groups, start=1):
        top = best_shifts_for_group(g, top_n=3)
        best_shift = top[0][0]
        best_key_nums.append(best_shift)

        # 输出该位的最优字母 + 备选
        candidates = ", ".join(
            f"{chr(s + ord('A'))}(chi2={sc:.2f})" for s, sc in top
        )
        print(f"Pos {idx}: {chr(best_shift + ord('A'))}    Top: {candidates}")

    key_guess = nums_to_text(best_key_nums)
    print("\nKey guess:", key_guess)


if __name__ == "__main__":
    main()
