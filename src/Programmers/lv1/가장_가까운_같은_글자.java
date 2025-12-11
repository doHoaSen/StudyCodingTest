package Programmers.lv1;
import java.util.*;

public class 가장_가까운_같은_글자 {
    class Solution {
        public int[] solution(String s) {
            int[] answer = new int[s.length()];
            for(int i = 0; i < s.length(); i++){
                // 인덱스 검사
                int idx = s.substring(0, i).lastIndexOf(s.charAt(i));
                if (idx == -1) answer[i] = -1;
                else {
                    answer[i] = i - idx;
                }
            }
            return answer;
        }
    }

    class Solution2 {
        public int[] solution(String s) {
            int[] answer = new int[s.length()];
            HashMap<Character, Integer> map = new HashMap<>();

            for(int i = 0; i < s.length(); i++){
                char c = s.charAt(i);
                answer[i] = i - map.getOrDefault(c, i+1);
                map.put(c, i);
            }
            return answer;
        }
    }
}
