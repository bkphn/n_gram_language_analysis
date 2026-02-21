from collections import Counter

import math
import numpy as np

VOWELS = set("aeiouyàáâãäåæèéêëìíîïòóôõöøùúûüýāąēėęěīįıōőœũūůűųοаеиоу")

YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def calculate_entropy(ngram_counts):
    total = sum(ngram_counts.values())
    entropy = 0

    for count in ngram_counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy

def characterise_clusters(groups, datasets, only_groups):

    for label, langs in sorted(groups.items()):
        total_words = 0
        total_letters = 0
        total_vowels = 0

        all_words_length = []
        all_suffixes = []
        all_prefixes = []
        all_max_consonant_clusters = []

        if only_groups:
            if len(langs) <= 1:
                continue

        all_ngrams = []
        for lang in langs:
            lang_key = lang.lower()
            words = datasets[lang_key]
            total_words += len(words)

            for word in words:
                word_lower = word.lower()

                letters_in_word = [char for char in word.lower() if char.isalpha()]
                all_words_length.append(len(letters_in_word))

                max_consonant_cluster = 0
                current_cluster = 0

                if len(letters_in_word) >= 3:
                    all_suffixes.append("".join(letters_in_word[-2:]))
                    all_prefixes.append("".join(letters_in_word[:2]))

                for char in letters_in_word:
                    total_letters += 1
                    if char in VOWELS:
                        total_vowels += 1
                        current_cluster = 0
                    else:
                        current_cluster += 1
                        if current_cluster > max_consonant_cluster:
                            max_consonant_cluster = current_cluster

                all_max_consonant_clusters.append(max_consonant_cluster)

                letters = [c for c in word.lower() if c.isalpha()]
                for i in range(len(letters) - 1):
                    all_ngrams.append("".join(letters[i:i + 2]))

        average_word_length = total_letters / total_words
        standard_deviation = np.std(all_words_length)
        vowel_percentage = (total_vowels / total_letters) * 100
        entropy = calculate_entropy(Counter(all_ngrams))
        average_max_consonant_cluster = np.mean(all_max_consonant_clusters)

        common_suffixes = Counter(all_suffixes).most_common(5)
        suffixes = ", ".join([f"'-{s[0]}'" for s in common_suffixes])

        common_prefixes = Counter(all_prefixes).most_common(5)
        prefixes = ", ".join([f"'{s[0]}-'" for s in common_prefixes])

        print(f"{BLUE}RODZINA: {', '.join(langs)}{RESET}")
        print(f" - Średnia długość słowa: {average_word_length:.2f} znaków")
        print(f" - Odchylenie standardowe długości słowa: {standard_deviation:.2f} znaków")
        print(f" - Procent samogłosek: {vowel_percentage:.1f}%")
        print(f" - Średnia najdłuższa zbitka spółgłoskowa: {average_max_consonant_cluster:.2f} znaków")
        print(f" - Najczęstsze prefiksy: {prefixes}")
        print(f" - Najczęstsze sufiksy: {suffixes}")
        print(f" - Entropia 2-gramowa: {entropy:.2f} bit")
        print("-" * 100)