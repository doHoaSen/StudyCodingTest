package programmers.lv2;
import java.util.*;

public class 영어끝말잇기 {

    class Solution {
        public int[] solution(int n, String[] words) {
            Set<String> used = new HashSet<>();
            used.add(words[0]);

            for(int i = 1; i < words.length; i++){
                if(words[i-1].charAt(words[i-1].length() -1) != words[i].charAt(0)
                        || used.contains(words[i])){
                    int person = i % n + 1;
                    int turn = i / n + 1;

                    return new int[]{person, turn};
                }
                used.add(words[i]);
            }

            return new int[]{0, 0};
        }
    }
}
