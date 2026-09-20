#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main () {
    int jogador
    int computador

    srand(time(0));

    cout << "=== JOKENPO ===" << endl;
    cout << "1 - Pedra" << endl;
    cout << "2 - Papel" << endl;
    cout << "3 - Tesoura" << endl;

    cout << "Escolha: ";
    cin >> jogador;

    computador = rand() % 3 + 1;

    cout << endl;

    if (jogador == 1) {
        cout << "Voce escolheu Pedra!" << endl;
    }
    else if (jogador == 2) {
        cout << "voce escolheu Papel!" << endl;
    }
    else if (jogador == 3) {
        cout << "Voce escolheu Tesoura!" << endl;
    }
    else{
        cout << "Opcao invalida!" << endl;
        return 0;
    }

    if (computador == 1) {
        cout << "Computador escolheu Pedra!" << endl;
    }
    else if (computador == 2) {
        cout << "Computador escolheu Papel!" << endl;
    }
    else {
        cout << "Computador escolheu Tesoura!" << endl;
    }

    cout << endl;

    if (jogador == computador) {
        cout << "EMPATE!" << endl;
    }
    else if (
        (jogador == 1 && computador == 3) ||
        (jogador == 2 && computador == 1) ||
        (jogador == 3 && computador == 2)
    ) {
        cout << "VOCE GANHOU!" << endl;
    }
    else {
        cout << "COMPUTADOR GANHOU!" << endl;
    }

    return 0;
}