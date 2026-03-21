import re
import os

def normalize(language):
    filename = os.path.join("Languages", language + ".txt")

    if not os.path.exists(filename):
        print(f"Plik {filename} nie istnieje.")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.readlines()

        data = [re.sub(r'^\d+\.\s*', '', line).split(' ')[0] for line in data if line.strip()]

        with open(filename, 'w', encoding='utf-8') as file:
            file.write('\n'.join(data))

        print(f"Pomyślnie znormalizowano {len(data)} słów, dla {language}.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def is_cyrillic(text):
    return bool(re.search(r'[\u0400-\u04FF]', text))

def cyryllic_filter(language):
    filename = os.path.join("Languages", language + ".txt")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = file.read().splitlines()

        data = []
        for word in words:
            if len(data) >= 15000:
                break
            elif is_cyrillic(word):
                continue
            else:
                data.append(word)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write('\n'.join(data))

        print(f"Pomyślnie przefiltrowano {len(data)} słów, dla {language}.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    running = True

    # cyryllic_filter("serbian")

    while running:
        language = input("Podaj język: ")
        normalize(language)

        state = input("\nCzy chcesz kontynuować normalizowanie? (y/n): ")
        if state.lower() == 'n':
            running = False