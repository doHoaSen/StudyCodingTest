package 프로그래머스.lv1;

public class 소수찾기 {
    class Solution {
        public int solution(int n) {
            int answer = 0;
            boolean flag = true;
            for(int i = 2; i <= n; i++){
                flag = isPrime(i);
                if (flag == true) answer++;
            }
            return answer;
        }

        public boolean isPrime(int n){
            if (n < 2) return false;
            if (n == 2) return true;

            for(int i = 2; i <= Math.sqrt(n); i++){
                if(n % i == 0) return false;
            }
            return true;
        }
    }
}
