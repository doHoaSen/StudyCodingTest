package 프로그래머스.lv1;

public class 로또의_최고순위와_최저순위 {
    class Solution {
        public int[] solution(int[] lottos, int[] win_nums) {

            int[] rank = {6, 6, 5, 4, 3, 2, 1};

            int zeroCnt = 0;
            int correct = 0;

            for (int n: lottos){
                if (n == 0) zeroCnt++;
                else {
                    for(int w: win_nums){
                        if (n == w) correct++;
                    }
                }
            }
            return new int[] {rank[correct + zeroCnt], rank[correct]};
        }
    }
}
