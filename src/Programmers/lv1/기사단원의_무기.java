package Programmers.lv1;

public class 기사단원의_무기 {
    class Solution {
        public int solution(int number, int limit, int power) {
            int answer = 0;
            // 약수 개수 구하기
            int divisor = 1;
            int[] divisors = new int [number+1];
            for(int i = 1; i <= number; i++){
                int cnt = 0;
                for(int k = 1; k*k <= i; k++){
                    if (i % k == 0){
                        cnt++;
                        if (k != i / k){
                            cnt++;
                        }
                    }
                }
                divisors[i] = cnt;
            }


            for(int n:divisors) System.out.print(n);

            // 약수 반복문 돌며 제한수치 비교
            for(int i = 1; i < divisors.length; i++){
                if (divisors[i] <= limit){
                    answer += divisors[i];
                } else {
                    answer += power;
                }
            }
            return answer;
        }
    }
}
