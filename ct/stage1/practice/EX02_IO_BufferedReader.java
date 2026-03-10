package ct.stage1.practice;

import java.util.*;
import java.io.*;


public class EX02_IO_BufferedReader {
    public static void main(String args[]) throws IOException{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int x = Integer.parseInt(st.nextToken());
        int y = Integer.parseInt(st.nextToken());

        System.out.println(x + y);
    }
}
