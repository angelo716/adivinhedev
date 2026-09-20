
#include <iostream>
#include <string>

int main() {
    int pergunta;

    std::cout << "=== Perguntas ===\n";
    std::cout << "1 - Qual a melhor fruta perm em custo beneficio do Blox Fruits?\n";
    std::cout << "2 - Qual o bounty maximo do Blox Fruits?\n";
    std::cout << "3 - Qual titulo se obtem quando se derrota um administrador do Blox Fruits?\n";
    std::cout << "4 - Qual a melhor gamepass em custo beneficio?\n";
    std::cout << "5 - Qual o nivel maximo da atualizacao 30?\n";

    std::cout << "Escolha uma pergunta: ";

    std::cin >> pergunta;

    std::cout << "\n";

    if (pergunta == 1) {
        std::cout << "Resposta: Dependendo do seu tipo de jogador, pode variar entre Buddha ou Portal.\n";
    }
    else if (pergunta == 2) {
        std::cout << "Resposta: 30 milhoes.\n";
    }
    else if (pergunta == 3) {
        std::cout << "Resp
