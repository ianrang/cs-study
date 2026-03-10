package java.part3a.section9hashSet.practice;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

public class SetSyncThreadSafeMain {
    final static int MAX_VALUE = 10000;
    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main thread started");
        SetThread setThread = new SetThread();

        Thread t1 = new Thread(() -> {
            System.out.println("Thread 1 started");
            for(int i = 0; i<MAX_VALUE; ++i){
                setThread.add("apple: "+i);
            }
            System.out.println("Thread 1 finished");
        });
        Thread t2 = new Thread(() -> {
            System.out.println("Thread 2 started");
            for(int i = 0; i<MAX_VALUE; ++i){
                setThread.add("banana: "+i);
            }
            System.out.println("Thread 2 finished");
        });

        t1.start();
        t2.start();
        Thread.sleep(10);
        t1.join();
        t2.join();

        System.out.println("size: "+setThread.getSize());
        System.out.println("Main thread finished");
    }
    public static class SetThread{
        Set<String> set = Collections.synchronizedSet(new HashSet<String>());
        public void add(String data){
            set.add(data);
        }
        public void remove(String data){
            set.remove(data);
        }
        public void print(){
            System.out.println(set);
        }

        public int getSize(){
            return set.size();
        }
    }
}