package 프로그래머스.lv1;

public class 푸드파이트대회 {
    class Solution {
        public String solution(int[] food) {
            StringBuilder sb = new StringBuilder();
            for(int i = 1; i < food.length; i++){
                int count = food[i] / 2;
                for(int j = 0; j < count; j++){
                    sb.append(i+"");
                }

            }
            sb = sb.append("0");
            String answer = sb.toString();
            for(int i = answer.length()-2; i >= 0; i--){
                answer += answer.charAt(i);
            }

            return answer;
        }
    }

    class Solution2 {
        public String solution(int[] food) {
            StringBuilder sb = new StringBuilder();
            for (int i = 1; i < food.length; i++) {
                int result = food[i] / 2;
                sb.append(String.valueOf(i).repeat(result));
            }
            String answer = sb + "0";
            return answer + sb.reverse();
        }
    }
}
