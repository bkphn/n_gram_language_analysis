import os

RED = '\033[91m \x1B[3m'
GREEN = '\033[92m \x1B[3m'
RESET = '\033[0m \x1B[0m'

def generate_datasets(languages, datasets):
    for language in languages:
        filename = os.path.join("Languages", language + ".txt")

        if not os.path.exists(filename):
            print(f"{RED}Plik {filename} nie istnieje.{RESET}")

        try:
            with open(filename, "r", encoding="utf-8") as file:
                datasets[language] = [line.strip() for line in file.readlines()]
                print(f"{GREEN}Wczytano {len(datasets[language])} słów dla: {language}{RESET}")
        except Exception as e:
            print(f"{RED}Wystąpił błąd: {e}{RESET}")

def bound_words(word_list):
    for i in range(len(word_list)):
        word = '#' + word_list[i] + '#'
        word_list[i] = word

def generate_ngrams(word_list, n):
    ngrams = []
    for word in word_list:
        ngrams.append([word[i:i + n] for i in range(len(word) - n + 1)])

    return ngrams
