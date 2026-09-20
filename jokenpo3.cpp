
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>

using namespace std;

int main() {
    string jogador;
    string computador;

    srand(time(0));

    cout << "=== JOKENPO ===" << endl;
    cout << "Digite pedra, papel ou tesoura: ";
    cin >> jogador;

    int escolha = rand() % 3 + 1;

    if (escolha == 1) {
        computador = "pedra";
    }
    else if (escolha == 2) {
        computador = "papel";
    }
    else {
        computador = "tesoura";
    }

    cout << endl;
    cout << "Voce escolheu: " << jogador << endl;
    cout << "Computador escolheu: " << computador << endl;

    cout << endl;

    if (jogador == computador) {
        cout << "EMPATE!" << endl;
    }
    else if (
        (jogador == "pedra" && computador == "tesoura") ||
        (jogador == "papel" && computador == "pedra") ||
        (jogador == "tesoura" && computador == "papel")
    ) {
        cout << "VOCE GANHOU!" << endl;
    }
    else if (
        jogador == "pedra" ||
        jogador == "papel" ||
        jogador == "tesoura"
    ) {
        cout << "COMPUTADOR GANHOU!" << endl;
    }
    else {
        cout << "OPCAO INVALIDA!" << endl;
    }

    return 0;
}