import numpy as np

D = ["Ala", "ma", "kota"]
N = [-1, 1]
d = 2
n = 0.1
ε = 50

V = np.array([[0.1, 0.2], [0.2, 0.2], [0.1, 0.3]])
Vp = np.array([[0.2, 0.1], [0.3, 0.1], [0.2, 0.2]])

for e in range(ε):
    for i in range(len(D)):
        print("---------------------------------------------------------")
        print(D[i], ":")

        # 1. Wyznaczanie prawdopodobieństwa
        print(" 1. Wyznaczanie prawdopodobieństwa")
        u = np.full(len(D), 0.0)
        p = np.full(len(D), 0.0)

        for j in range(len(D)):
            u[j] = np.round(Vp[j] @ V[i],5)
            print("\t", f"u({D[j]} | {D[i]}) = {u[j]}")

        print()
        for j in range(len(D)):
            p[j] = np.round(np.exp(u[j]) / np.sum(np.exp(u)), 4)

            print("\t", f"P({D[j]}|{D[i]}) = {p[j]}")

        print("\n\t", f"p = {p}")

        # 2. Wyznaczanie błędu
        print("\n 2. Wyznaczanie błędu")
        t = np.full(len(D), 0.0)
        δ = np.full(len(D), 0.0)

        K = []
        for j in N:
            if len(D) > i + j and i + j >= 0:
                print(D[i + j])
                K += [D[i + j]];

        for j in range(len(D)):
            if D[j] in K:
                t[j] = 1.0
        print("\t", f"t_{D[i]} = {t}")

        δ = len(K) * p - t
        print("\t", f"δ_{D[i]} = {δ}")

        # 3. Aktualizacja macierzy wag
        print("\n 3. Aktualizacja macierzy wag")

        grad_v = δ @ Vp
        print("\t", f"∇v_{D[i]} = {grad_v}\n")

        grad_Vp = np.outer(δ, V[i])
        print("\t", f"∇V' =\n{grad_Vp}")

        print("\n--- WYNIK ---\n")

        V[i] -= n * grad_v
        print("\t", f"V =\n{V}\n")

        Vp -= n * grad_Vp
        print("\t", f"Vp =\n{Vp}")