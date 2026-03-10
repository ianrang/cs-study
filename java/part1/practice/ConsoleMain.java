package java.part1.practice;

import java.io.IOException;

public class ConsoleMain {
    public static void main(String[] args) throws IOException {
        char keycode = (char) System.in.read();
        System.out.println(keycode);
        keycode = (char) System.in.read();
        System.out.println(keycode);
        keycode = (char) System.in.read();
        System.out.println(keycode);
    }
}
