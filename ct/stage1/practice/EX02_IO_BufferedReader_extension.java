package ct.stage1.practice;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class EX02_IO_BufferedReader_extension {
    public static void main(String[] args) throws IOException{
        initBuffer();
        
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        while(br.ready()){
            String line = br.readLine();
            StringTokenizer st = new StringTokenizer(line);
            while(st.hasMoreTokens()){
                System.out.println(st.nextToken());
            }
        }
    }
    public static void initBuffer(){
        String input = "10,20,30\n40,50,60\n";
        System.setIn(new ByteArrayInputStream(input.getBytes()));
    }
}
