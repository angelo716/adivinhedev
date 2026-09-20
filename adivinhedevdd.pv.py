
import random

def jogar():
    numero_secreto = random.randint(1, 100)
    chances = 10
    tentativas = 0

    print("\n=== ADIVINHE O NÚMERO ===")
    nome = input("Digite seu nome: ")

    print(f"\nFala, {nome}! Pensei em um número de 1 a 100.")
    print(f"Você tem {chances} chances!")

    while tentativas < chances:
        try:
            palpite = int(input("\nSeu palpite: "))
        except ValueError:
            print("Digite um número válido!")
            continue

        if palpite < 1 or palpite > 100:
            print("Escolha um número entre 1 e 100!")
            continue

        tentativas += 1
        chances_restantes = chances - tentativas

        if palpite < numero_secreto:
            print("É MAIOR!")
        elif palpite > numero_secreto:
            print("É MENOR!")
        else:
            nota = 110 - tentativas * 10

            print("\n🎉 VOCÊ ACERTOU!")
            print("Jogador:", nome)
            print("Número secreto:", numero_secreto)
            print("Tentativas usadas:", tentativas)
            print("Nota de eficiência:", nota)

            return {
                "nome": nome,
                "tentativas": tentativas,
                "nota": nota
            }

        print("Chances restantes:", chances_restantes)

    print("\nGAME OVER! 😭")
    print("O número era:", numero_secreto)

    return {
        "nome": nome,
        "tentativas": tentativas,
        "nota": 0
    }


while True:
    resultado = jogar()

    print("\n=== RESULTADO ===")
    print("Jogador:", resultado["nome"])
    print("Nota:", resultado["nota"])

    novamente = input("\nJogar novamente? (s/n): ").lower()

    if novamente != "s":
        print("Valeu por jogar! 🦫")
        break

