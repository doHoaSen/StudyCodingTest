package programmers.lv1;
import java.util.*;

public class 신고결과받기 {

    class Solution {
        public int[] solution(String[] id_list, String[] report, int k) {

            // 신고 중복 제거
            Set<String> uniqueReports = new HashSet<>(Arrays.asList(report));

            // 신고 당한 사람 -> 신고한 사람들 집합
            Map<String, HashSet<String>> reportedBy = new HashMap<>();
            for (String id : id_list) {
                reportedBy.put(id, new HashSet<>());
            }

            for (String r : uniqueReports) {
                String[] parts = r.split(" ");
                String from = parts[0]; // 신고한 사람
                String to = parts[1];   // 신고당한 사람
                reportedBy.get(to).add(from);
            }

            // 메일 개수
            Map<String, Integer> mailCount = new HashMap<>();
            for (String id : id_list) {
                mailCount.put(id, 0);
            }

            // 정지 대상 찾고 메일 분배
            for (String user : id_list) {
                if (reportedBy.get(user).size() >= k) {
                    for (String reporter : reportedBy.get(user)) {
                        mailCount.put(reporter, mailCount.get(reporter) + 1);
                    }
                }
            }

            // id_list 순서대로 결과 생성
            int[] answer = new int[id_list.length];
            for (int i = 0; i < id_list.length; i++) {
                answer[i] = mailCount.get(id_list[i]);
            }

            return answer;
        }
    }

}
