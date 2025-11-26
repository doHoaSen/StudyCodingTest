package 프로그래머스.lv1;

public class 콜라문제 {
    class Solution {
        public int solution(int a, int b, int n) {
            int answer = 0;

            while (n >= a){
                int exchanged = n / a * b;
                answer += exchanged;
                n = exchanged + (n % a);
            }
            return answer;
        }
    }
}
