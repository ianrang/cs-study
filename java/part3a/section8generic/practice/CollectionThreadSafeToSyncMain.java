package java.part3a.section8generic.practice;

import java.util.ArrayList;

public class CollectionThreadSafeToSyncMain {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main thread started");

        CollectionThread ct = new CollectionThread();

        Thread t1 = new Thread(() -> {
            System.out.println("Thread 1 started");
            ct.addTestDataToList();
            System.out.println("Thread 1 finished");
        });

        Thread t2 = new Thread(() -> {
            System.out.println("Thread 2 started");
            ct.addDataToList();
            System.out.println("Thread 2 finished");
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("size: "+ct.getSize());
        System.out.println("Main thread finished");
    }

    public static class CollectionThread{
        ArrayList<String> list = new ArrayList<>();
        final int MAX_VALUE = 10000;

        public synchronized void addTestDataToList(){
            for(int i = 0; i<MAX_VALUE; ++i){
                list.add("test: "+i);
            }     
        }
        
        public synchronized void addDataToList(){
            for(int i = 0; i<MAX_VALUE; ++i){
                list.add("data: "+i);
            }     
        }

        public int getSize(){
            return list.size();
        }
    }
}

