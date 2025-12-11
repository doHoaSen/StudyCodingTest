package programmers.lv1;
import java.util.*;

public class 실패율 {
    class Solution {
        public int[] solution(int N, int[] stages) {
            // 스테이지별 머무르는 사람: count[] 사용
            int[] count = new int[N+2]; // N+1은 클리어한 사용자
            for(int s : stages){
                count[s]++;
            }

            // 결과 저장용 리스트
            List<double[]> list = new ArrayList<>();
            int players = stages.length;

            // 실패율
            for(int i = 1; i <= N; i++){
                double failRate = 0.0;
                if(players > 0){
                    failRate = (double) count[i] / players;
                }
                list.add(new double[]{i, failRate});
                players -= count[i];
            }

            // 스테이지 번호 실패율의 내림차순 정렬
            Collections.sort(list, (a, b) -> {
                if(a[1] == b[1]) return Double.compare(a[0], b[0]);
                return Double.compare(b[1], a[1]);
            });

            int[] answer = new int[N];
            for(int i = 0; i < N; i++){
                answer[i] = (int)list.get(i)[0];
            }
            return answer;
        }
    }
}
