import os

def clear_raport():
    os.makedirs("Raports", exist_ok=True)

    with open(os.path.join("Raports", "raport.txt"), "w", encoding="utf-8") as file:
        pass

def raport_only(text):
    os.makedirs("Raports", exist_ok=True)

    with open(os.path.join("Raports", "raport.txt"), "a", encoding="utf-8") as file:
        file.write(str(text) + "\n")

def raport(text):
    print(text)

    os.makedirs("Raports", exist_ok=True)

    with open(os.path.join("Raports", "raport.txt"), "a", encoding="utf-8") as file:
        file.write(str(text) + "\n")