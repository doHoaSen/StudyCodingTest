package programmers.lv1;

public class 요일구하기_2016년 {
    class Solution {
        public String solution(int a, int b) {
            int answer = 0;
            String[] days = {"FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"};
            int[] months = {31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 30};

            for(int i = 0; i < a - 1; i++){
                answer += months[i];
            }

            answer += b - 1;

            return days[answer%7];
        }
    }
}
