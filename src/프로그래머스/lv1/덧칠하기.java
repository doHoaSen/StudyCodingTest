package 프로그래머스.lv1;

public class 덧칠하기 {
    class Solution {
        public int solution(int n, int m, int[] section) {
            int cnt = 0;
            int roller = section[0];
            cnt += 1;

            for(int i = 1; i <section.length; i++){
                if(roller + m - 1 < section[i]){
                    cnt += 1;
                    roller = section[i];
                }
            }

            return cnt;
        }
    }
}
