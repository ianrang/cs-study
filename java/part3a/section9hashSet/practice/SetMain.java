package java.part3a.section9hashSet.practice;

import java.util.HashSet;
import java.util.Iterator;

public class SetMain {
    public static void main(String[] args) {
        HashSet<String> set = new HashSet<>();
        set.add("apple");
        set.add("banana");
        set.add("cherry");
        System.out.println(set);

        Iterator<String> iterator = set.iterator();
        while(iterator.hasNext()){
            System.out.println(iterator.next());
        }
    }
}