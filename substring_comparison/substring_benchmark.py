import timeit
from pathlib import Path

def boyer_moore(text, pattern):
    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0

    if m > n:
        return -1

    bad_char = {char: index for index, char in enumerate(pattern)}
    shift = 0

    while shift <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            return shift

        shift += max(1, j - bad_char.get(text[shift + j], -1))

    return -1

def kmp(text, pattern):
    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0

    if m > n:
        return -1

    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    i = 0
    j = 0

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                return i - j

        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1

    return -1

def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0

    if m > n:
        return -1

    base = 256
    modulus = 1_000_000_007
    high = pow(base, m - 1, modulus)

    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (
            pattern_hash * base + ord(pattern[i])
        ) % modulus

        window_hash = (
            window_hash * base + ord(text[i])
        ) % modulus

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            window_hash = (
                (window_hash - ord(text[i]) * high) * base
                + ord(text[i + m])
            ) % modulus

    return -1

def read_article(filename):
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(
            f"File '{filename}' was not found."
        )

    return path.read_text(encoding="utf-8")

def benchmark(algorithm, text, pattern):
    runs = timeit.repeat(
        lambda: algorithm(text, pattern),
        number=100,
        repeat=5,
    )

    return min(runs) / 100


def main():
    algorithms = {
        "Boyer-Moore": boyer_moore,
        "KMP": kmp,
        "Rabin-Karp": rabin_karp,
    }

    articles = {
        "Article 1": read_article("article1.txt"),
        "Article 2": read_article("article2.txt"),
    }

    absent_pattern = "XYZ_ABSENT_PATTERN_987654321"

    for article_name, text in articles.items():
        start = len(text) // 2
        existing_pattern = text[start:start + 20]

        while not existing_pattern.strip() and start > 0:
            start -= 1
            existing_pattern = text[start:start + 20]

        tests = {
            "Existing substring": existing_pattern,
            "Absent substring": absent_pattern,
        }

        print(f"\n{'=' * 65}")
        print(f"{article_name} (length: {len(text)} characters)")
        print(f"{'=' * 65}")

        for test_name, pattern in tests.items():
            print(f"\nTest: {test_name}")
            print(f"Pattern: {pattern!r}")

            results = []

            for name, algorithm in algorithms.items():
                result = algorithm(text, pattern)
                assert result == text.find(pattern), (
                    f"{name} returned an incorrect result."
                )

                elapsed = benchmark(algorithm, text, pattern)
                microseconds = elapsed * 1_000_000

                results.append((name, microseconds))

                print(
                    f"{name:15} | "
                    f"Position: {result:7} | "
                    f"Time: {microseconds:10.3f} microseconds"
                )

            fastest = min(results, key=lambda item: item[1])

            print(
                f"Fastest for this test: "
                f"{fastest[0]} ({fastest[1]:.3f} microseconds)"
            )

    print("\nAll algorithms passed the correctness checks.")


if __name__ == "__main__":
    main()