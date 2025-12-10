package 이코테_자바.chapter6;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class 정렬라이브러리에서_key활용_6_9 {
    public static void main(String args[]){
        List<Item> list = new ArrayList<>();
        list.add(new Item("banana", 2));
        list.add(new Item("apple", 5));
        list.add(new Item("carrot", 3));

        list.sort(Comparator.comparingInt(Item::getScore));

        for(Item item: list){
            System.out.println(item.name + " " + item.score);
        }
    }
}

class Item{
    String name;
    int score;

    public Item(String name, int score){
        this.name = name;
        this.score = score;
    }

    int getScore(){
        return score;
    }
}