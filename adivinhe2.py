import random

numero_secreto = random.randint(1, 100)
tentativas = 0

print("=== ADIVINHE O NUMERO ===")
print("Eu escolhi um numero entre 1 a 100!")

while True:
    palpite = int(input("Digite seu palpite: "))
    tentativas += 1

    if palpite < numero_secreto:
        print("É MAIOR!")

    elif palpite > numero_secreto:
        print("É MENOR!")

    else:
        print("VOCE ACERTOU! :)")
        print("Numero secreto:", numero_secreto)
        print("Tentativas:", tentativas)
        break