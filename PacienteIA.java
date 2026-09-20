import java.util.Scanner;
import java.util.Random;

public class PacienteIA {

    static Scanner scanner = new Scanner(System.in);
    static Random random = new Random();

    // Perfil do paciente fictício
    static String nome = "Lucas";
    static int idade = 24;

    static String[] respostas = {
        "Eu não sei muito bem como explicar... tenho me sentido meio estranho ultimamente.",
        "Acho que tenho pensado demais nas coisas. Minha cabeça não para.",
        "Tem dias em que eu acordo sem muita vontade de fazer nada.",
        "Eu sinto que as pessoas esperam muito de mim.",
        "Às vezes eu prefiro ficar sozinho, mas nem sei exatamente por quê.",
        "Eu tenho dificuldade para falar sobre isso com as pessoas.",
        "Quando isso acontece, eu fico pensando que talvez o problema seja comigo.",
        "Não sei... acho que nunca contei isso para ninguém.",
        "Eu tento me distrair, mas os pensamentos acabam voltando.",
        "Talvez eu esteja exagerando. Não sei."
    };

    public static void main(String[] args) {

        System.out.println("======================================");
        System.out.println("       TREINAMENTO - PACIENTE IA");
        System.out.println("======================================");
        System.out.println();

        System.out.println("Paciente: " + nome);
        System.out.println("Idade: " + idade);
        System.out.println();

        System.out.println("IA: Oi... acho que podemos começar.");
        System.out.println("IA: Você pode conversar comigo como se eu fosse seu paciente.");
        System.out.println("IA: Quando quiser terminar, digite 'sair'.");
        System.out.println();

        while (true) {

            System.out.print("Psicólogo: ");
            String pergunta = scanner.nextLine();

            if (pergunta.equalsIgnoreCase("sair")) {
                System.out.println();
                System.out.println("IA: Acho que podemos parar por aqui.");
                System.out.println("Sessão encerrada.");
                break;
            }

            String resposta = gerarResposta(pergunta);

            System.out.println();
            System.out.println("Paciente IA: " + resposta);
            System.out.println();
        }

        scanner.close();
    }

    static String gerarResposta(String pergunta) {

        String texto = pergunta.toLowerCase();

        // Respostas baseadas no que o psicólogo perguntou
        if (texto.contains("nome")) {
            return "Meu nome é " + nome + "... tenho " + idade + " anos.";
        }

        if (texto.contains("como você está") ||
            texto.contains("como voce esta")) {

            return "Ultimamente eu não tenho me sentido muito bem. " +
                   "Não sei exatamente o que está acontecendo.";
        }

        if (texto.contains("família") ||
            texto.contains("familia")) {

            return "Minha família é meio complicada. " +
                   "Eu gosto deles, mas às vezes sinto que não consigo conversar com eles.";
        }

        if (texto.contains("trabalho") ||
            texto.contains("faculdade") ||
            texto.contains("estudo")) {

            return "Tenho sentido bastante pressão com isso. " +
                   "Às vezes parece que não estou conseguindo acompanhar tudo.";
        }

        if (texto.contains("amigos")) {
            return "Eu tenho alguns amigos, mas ultimamente tenho me afastado um pouco.";
        }

        if (texto.contains("por quê") ||
            texto.contains("por que") ||
            texto.contains("porque")) {

            return "Eu mesmo não sei explicar direito. " +
                   "Talvez seja algo que venho sentindo há bastante tempo.";
        }

        // Caso não reconheça a pergunta,
        // escolhe uma resposta aleatória
        return respostas[random.nextInt(respostas.length)];
    }
}