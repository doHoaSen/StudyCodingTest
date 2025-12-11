package Programmers.lv1;
import java.util.*;

public class 추억점수 {

    class Solution {
        public int[] solution(String[] name, int[] yearning, String[][] photo) {
            int[] answer = new int[photo.length];

            HashMap<String, Integer> memory = new HashMap<>();
            for(int i = 0; i < name.length; i++){
                memory.put(name[i], yearning[i]);
            }

            for(int i = 0; i < photo.length; i++){
                int score = 0;
                for(int j = 0; j < photo[i].length; j++){
                    if (memory.containsKey(photo[i][j])){
                        score += memory.get(photo[i][j]);
                    }
                }
                answer[i] = score;
            }


            return answer;
        }
    }
}
