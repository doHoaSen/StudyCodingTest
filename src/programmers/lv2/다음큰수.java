package programmers.lv2;

public class 다음큰수 {
    class Solution {
        public int solution(int n) {
            int answer = n + 1;
            int count = Integer.bitCount(n);

            while(true){
                if (count == Integer.bitCount(answer)){
                    break;
                }
                answer++;
            }
            return answer;
        }
    }
}
