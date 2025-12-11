package Programmers.lv1;
import java.util.*;

public class 대충만든자판 {
    class Solution {
        public int[] solution(String[] keymap, String[] targets) {
            int[] answer = new int[targets.length];
            int i = 0;
            for(String target: targets){
                int total = 0;
                for(char c: target.toCharArray()){
                    int min_press = Integer.MAX_VALUE;
                    for(String key: keymap){
                        int idx = key.indexOf(c);
                        if (idx != -1){
                            min_press = Math.min(min_press, idx+1);
                        }
                    }
                    if (min_press == Integer.MAX_VALUE) {
                        total = -1;
                        break;
                    }

                    total += min_press;
                }
                answer[i] = total;
                i++;
            }

            return answer;
        }
    }


    class Solution2 {
        public int[] solution(String[] keymap, String[] targets) {
            int[] answer = new int[targets.length];
            // 문자별 최소 클릭 수 계산
            HashMap<Character, Integer> map = new HashMap<>();

            for(String key: keymap){
                for(int i = 0; i < key.length(); i++){
                    char c = key.charAt(i);
                    int press = i+1;

                    map.put(c, Math.min(map.getOrDefault(c, Integer.MAX_VALUE), press));
                }
            }

            // target별 계산
            for(int t = 0; t < targets.length; t++){
                int total = 0;
                for(char c: targets[t].toCharArray()){
                    if(!map.containsKey(c)){
                        total = -1;
                        break;
                    }
                    total += map.get(c);
                }
                answer[t] = total;
            }

            return answer;
        }
    }
}
