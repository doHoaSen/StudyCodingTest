package programmers.lv2;

public class 탐욕법_조이스틱 {
    class Solution {
        public int solution(String name) {
            int move = 0;
            // 이동: min(A->B, A->Z)

            // 세로 이동
            for(int i = 0; i < name.length(); i++){
                char c = name.charAt(i);
                move+= Math.min(c-'A', 'Z'-c+1);
            }

            // 가로 이동
            int n = name.length();
            int minMove = n - 1; // 왼 -> 오
            for(int i = 0; i < n; i++){
                int nextIdx = i+1;
                // A 연속으로 나오는 구간
                while(nextIdx < n && name.charAt(nextIdx) == 'A'){
                    nextIdx++;
                }

                // 되돌아가기1: 오 -> 왼
                int case1 = 2 * i + (n - nextIdx);
                // 되돌아가기2: 왼 -> 오
                int case2 = (n - nextIdx) * 2 + i;


                minMove = Math.min(minMove, Math.min(case1, case2));
            }


            return move + minMove;
        }
    }
}
