print("===CALCULADORA===")

numero1 = float(input("Digite o primeiro numero: "))
operacao = input("Digite a operaçao (+, -, *, /): ")
numero2 = float(input("Digite o segundo numero: "))

if operacao == "+":
    resultado = numero1 + numero2

elif operacao == "-":
    resultado = numero1 - numero2
elif operacao == "*":
    resultado = numero1 * numero2

elif operacao == "/":
    resultado = numero1 / numero2

else:
    resultado = "operaçao invalida!"

print("Resultado:", resultado)