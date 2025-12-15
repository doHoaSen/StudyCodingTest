package programmers.lv1;

public class 유연근무제 {
    class Solution {
        public int solution(int[] schedules, int[][] timelogs, int startday) {
            int answer = 0;
            for(int i = 0; i < timelogs.length; i++){
                boolean ok = true;

                int limit = calcLimit(schedules[i]);

                for(int d = 0; d < 7; d++){
                    int today = (startday + d - 1) % 7 + 1;
                    if (today == 6 || today == 7) continue;
                    int actual = timelogs[i][d];
                    if (actual > limit){
                        ok = false;
                        break;
                    }
                }
                if (ok){
                    answer++;
                }
            }
            return answer;
        }

        public int calcLimit(int want){
            int hour = want / 100;
            int min = want % 100;

            min += 10;
            if (min >= 60){
                hour++;
                min -= 60;
            }
            return hour * 100 + min;
        }
    }
}
