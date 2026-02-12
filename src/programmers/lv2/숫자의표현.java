package programmers.lv2;

public class 숫자의표현 {
    class Solution {
        public int solution1(int n) {
            int answer = 0;
            for(int k = 1; k * (k + 1) / 2 <= n; k++){
                int numerator = n - k * (k - 1) / 2;
                if (numerator % k == 0) answer++;
            }
            return answer;
        }

        public int solution2(int n){
            int answer = 0;
            for(int i = 1; i <= n; i++){
                int sum = 0;
                for(int j = i; j <= n; j++){
                    sum += j;

                    if (sum >= n){
                        if (sum == n) answer++;
                        break;
                    }
                }
            }
            return answer;
        }

        // 슬라이딩 윈도우
        public int solution3(int n){
            int sum = 0;
            int answer = 0;
            int left = 0;

            for(int i = 1; i <= n; i++){
                sum += i;

                while(sum > n){
                    sum -= left;
                    left++;
                }

                if (sum == n) answer++;
            }

            return answer;
        }
    }
}
