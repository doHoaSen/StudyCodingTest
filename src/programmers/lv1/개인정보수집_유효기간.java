package programmers.lv1;
import java.util.*;

public class 개인정보수집_유효기간 {

    class Solution {
        public int[] solution(String today, String[] terms, String[] privacies) {
            int todayValue = convert(today);
            // 약관 유효기간 저장
            Map<String, Integer> termMap = new HashMap<>();
            for(String t : terms){
                String[] arr = t.split(" ");
                termMap.put(arr[0], Integer.parseInt(arr[1]));
            }

            List<Integer> result = new ArrayList<>();

            // 개인정보 하나씩 검사
            for(int i = 0; i < privacies.length; i++){
                String[] arr = privacies[i].split(" ");

                String date = arr[0];
                String termType = arr[1];

                int collectValue = convert(date);
                int expireValue = collectValue + termMap.get(termType) * 28;

                if (expireValue <= todayValue) result.add(i+1);
            }

            int[] answer = new int[result.size()];

            for(int i = 0; i < result.size(); i++) answer[i] = result.get(i);
            return answer;
        }

        private int convert (String date){
            String[] arr = date.split("\\.");
            int y = Integer.parseInt(arr[0]);
            int m = Integer.parseInt(arr[1]);
            int d = Integer.parseInt(arr[2]);

            return d + m * 28 + y * 28 * 12;
        }
    }
}
