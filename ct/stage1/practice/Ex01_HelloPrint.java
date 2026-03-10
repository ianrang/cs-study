package ct.stage1.practice;

public class Ex01_HelloPrint {
    public static void main(String[] args){
        if(args.length > 0){
            System.out.println("====");
            System.out.println("My name is " + args[0]); 
            System.out.println("====");
        }
        else{
            System.out.println("No name");
        }
    }
}