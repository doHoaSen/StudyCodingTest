package 프로그래머스.lv1;

import java.util.Arrays;

public class 예산 {
    public int solution(int[] d, int budget) {
        int answer = 0;
        Arrays.sort(d);

        for (int cost: d){
            if (budget >= cost){
                budget -= cost;
                answer++;
            } else {
                break;
            }
        }
        return answer;
    }
}
