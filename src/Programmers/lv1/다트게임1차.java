package Programmers.lv1;
import java.util.*;

public class 다트게임1차 {
    class Solution {
        public int solution(String dartResult) {
            int score = 0;
            ArrayList<Integer> scores = new ArrayList<>();

            for(int i = 0; i < dartResult.length(); i++){
                char c = dartResult.charAt(i);
                // 숫자 판별
                if(Character.isDigit(c)){
                    // 10점일 경우
                    if (c == '1' && i+1<dartResult.length() && dartResult.charAt(i+1) == '0'){
                        score = 10;
                        i++;
                    } else {
                        score = c - '0';
                    }
                }
                // S, D, T인 경우
                else if (c == 'S'){
                    score = (int)Math.pow(score, 1);
                    scores.add(score);
                } else if (c == 'D'){
                    score = (int)Math.pow(score, 2);
                    scores.add(score);
                } else if (c == 'T'){
                    score = (int)Math.pow(score, 3);
                    scores.add(score);
                }

                // *, # 인 경우
                else if (c == '*'){
                    int lastIndex = scores.size() - 1;
                    // 현재 점수 수정
                    scores.set(lastIndex, scores.get(lastIndex) * 2);
                    // 이전 점수 수정
                    if (scores.size() > 1){
                        scores.set(lastIndex - 1, scores.get(lastIndex-1) * 2);
                    }
                } else if (c == '#'){
                    int lastIndex = scores.size() - 1;
                    // 현재 점수 수정
                    scores.set(lastIndex, scores.get(lastIndex) * -1);
                }
            }

            int total = 0;
            for(int t: scores){
                total += t;
            }

            return total;
        }
    }
}
