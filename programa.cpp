```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Digite um numero:");
        System.out.println("1 - Qual a pior academia de PvP de 2025/2026?");
        System.out.println("2 - Onde se inscrever para ter um bom ensino de PvP?");
        System.out.println("3 - Quem representou o Brasil em 2025 e 2026 no mundial?");

        int numero = scanner.nextInt();

        if (numero == 1) {
            System.out.println("The Ocean Academy, pela sua pessima reputacao.");
        } 
        else if (numero == 2) {
            System.out.println("Na academia 'Kamizys', do professor Emokami.");
        } 
        else if (numero == 3) {
            System.out.println("Professor_vicz e Emokami.");
        } 
        else {
            System.out.println("Opcao invalida.");
        }

        scanner.close();
    }
}
```
