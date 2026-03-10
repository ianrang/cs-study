package java.part3a.section8generic.practice;

public class GenericMain {
    public static void main(String[] args) {
        MyData<String> myData = new MyData<>();
        myData.setData("Hello, World!");
        System.out.println(myData.getData());

        MyData<Integer> myData2 = new MyData<>();
        myData2.setData(1234);
        System.out.println(myData2.getData());
    }
    
    public static class MyData<T> {
        private T data;
    
        public T getData() {
            return data;
        }
    
        public void setData(T data) {
            this.data = data;
        }
    }
}

