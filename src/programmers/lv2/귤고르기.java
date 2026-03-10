package programmers.lv2;
import java.util.*;

public class 귤고르기 {
    class Solution {
        public int solution(int k, int[] tangerine) {
            // 빈도 계산
            Map<Integer, Integer> map = new HashMap<>();
            for(int t: tangerine){
                map.put(t, map.getOrDefault(t, 0) + 1);
            }

            // 빈도 리스트
            List<Integer> counts = new ArrayList<>(map.values());
            counts.sort(Collections.reverseOrder()); // 내림차순

            int answer = 0;
            for(int cnt: counts){
                k -= cnt;
                answer++;
                if (k <= 0) break;
            }
            return answer;
        }
    }
}
