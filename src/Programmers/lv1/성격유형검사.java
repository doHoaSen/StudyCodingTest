package programmers.lv1;
import java.util.*;

public class 성격유형검사 {

    class Solution {
        public String solution(String[] survey, int[] choices) {

            // 점수 누적 Map
            HashMap<Character, Integer> scores = new HashMap<>();
            for(char c: "RTCFJMAN".toCharArray()){
                scores.put(c, 0);
            }

            // survey마다 점수
            for(int i = 0; i < survey.length; i++){
                char left = survey[i].charAt(0);
                char right = survey[i].charAt(1);
                int choice = choices[i];

                if (choice < 4){
                    // 비동의
                    scores.put(left, scores.get(left) + (4 - choice));
                } else if (choice > 4){
                    // 동의
                    scores.put(right, scores.get(right) + (choice - 4));
                }
            }

            // 선택
            StringBuilder sb = new StringBuilder();
            sb.append(scores.get('R') >= scores.get('T') ? "R": "T");
            sb.append(scores.get('C') >= scores.get('F') ? "C": "F");
            sb.append(scores.get('J') >= scores.get('M') ? "J": "M");
            sb.append(scores.get('A') >= scores.get('N') ? "A": "N");

            return sb.toString();
        }
    }
}
