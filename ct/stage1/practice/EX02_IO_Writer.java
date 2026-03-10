package ct.stage1.practice;

import java.util.*;
import java.io.*;

public class EX02_IO_Writer {
    public static void main(String args[]) throws IOException {
        BufferedWriter  bw = new BufferedWriter(new OutputStreamWriter(System.out));
        bw.write("Hello World");
        bw.close();
    }
}
