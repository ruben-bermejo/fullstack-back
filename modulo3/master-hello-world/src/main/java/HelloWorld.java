public class HelloWorld {
    public static void main(String[] args) {
        // Muestra por consola Hello, World
        TextService textService = new TextService("Hola, Mundo");
        System.out.println(textService.getTexto());
    }
}
