package Programmers.lv1;

public class 비밀지도1차 {
    class Solution {
        public String[] solution(int n, int[] arr1, int[] arr2) {
            String[] answer = new String[n];

            for (int i = 0; i < n; i++) {
                int line = arr1[i] | arr2[i];
                StringBuilder sb = new StringBuilder();

                for (int j = n - 1; j >= 0; j--) {
                    // j번째 비트가 1인지 확인
                    if ((line & (1 << j)) != 0) sb.append("#");
                    else sb.append(" ");
                }

                answer[i] = sb.toString();
            }
            return answer;
        }
    }
}
