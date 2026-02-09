package programmers.lv2;

public class 이진변환반복하기 {
    class Solution {
        public int[] solution(String s) {
            int[] answer = new int[2];
            int cnt = 0;
            int zero = 0;
            StringBuilder sb;
            while(!s.equals("1")){
                sb = new StringBuilder();
                for(int i = 0; i < s.length(); i++){
                    if (s.charAt(i) == '0'){
                        zero++;
                    } else{
                        sb.append(s.charAt(i));
                    }
                }

                s = Integer.toBinaryString(sb.length());
                cnt++;

            }

            answer[0] = cnt;
            answer[1] = zero;
            return answer;
        }
    }

    class Solution2 {
        public int[] solution(String s) {
            int[] answer = new int[2];
            int cnt = 0;
            int zero = 0;

            while(!s.equals("1")){
                int ones = 0;
                for(char c: s.toCharArray()){
                    if (c == '0') zero++;
                    else ones++;
                }

                s = Integer.toBinaryString(ones);
                cnt++;

            }

            answer[0] = cnt;
            answer[1] = zero;
            return answer;
        }
    }
}
