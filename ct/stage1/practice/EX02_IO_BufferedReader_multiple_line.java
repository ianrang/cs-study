package ct.stage1.practice;

import java.util.*;
import java.io.*;

public class EX02_IO_BufferedReader_multiple_line{
    public static void main(String args[]) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int n = Integer.parseInt(br.readLine().trim());

        for(int i = 0; i<n; ++i){
            String line = br.readLine();
            System.out.println(line);
        }
    }
}
