package ct.stage1.practice.ex;

import java.io.*;
import java.util.*;

public class EX02_ex {
    public static void main(String[] args){
        try{
            assignment_01();
            asignment_02();
        }
        catch(Exception ex){

        }
    }

    // ### 과제 1: Scanner 사용
    // 정수 3개를 입력받아 합계와 평균을 출력하는 프로그램을 Scanner로 작성하라.
    public static void assignment_01() throws IOException {
        Scanner sc = new Scanner(System.in);

        final int count = 3;
        int sum = 0;
        for(int i = 0; i < count; ++i ){
            sum += sc.nextInt();
        }
        System.out.println(sum);
    }

    // ### 과제 2: BufferedReader로 변환
    // 과제 1을 BufferedReader + StringTokenizer로 다시 작성하라.
    public static void asignment_02() throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        StringTokenizer st = new StringTokenizer(br.readLine());
        int sum = 0;
        while(st.hasMoreTokens()){
            sum += Integer.parseInt(st.nextToken());
        }
        System.out.println(sum);
    }
}
