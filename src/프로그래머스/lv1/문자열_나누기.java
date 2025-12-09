package 프로그래머스.lv1;

public class 문자열_나누기 {
    class Solution {
        public int solution(String s) {
            int answer = 0;

            char x = s.charAt(0);
            int cntElse = 0;
            int cntX = 0;

            for(int i = 0; i < s.length(); i++){
                if(x == s.charAt(i)) cntX++;
                else cntElse++;

                if (cntX == cntElse){
                    answer++;
                    cntX = 0;
                    cntElse = 0;
                    if (i + 1 < s.length()) x = s.charAt(i+1);
                }
            }

            if(cntX != 0 || cntElse != 0) answer++;

            return answer;
        }
    }
}
