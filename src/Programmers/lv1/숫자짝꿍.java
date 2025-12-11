package Programmers.lv1;

public class 숫자짝꿍 {
    class Solution {
        public String solution(String X, String Y) {
            int[] countx = new int [10];
            int[] county = new int [10];

            // 개수 세기
            for (char x : X.toCharArray()){
                countx[x-'0']++;
            }

            for (char y: Y.toCharArray()){
                county[y-'0']++;
            }

            // 공통 숫자
            StringBuilder sb = new StringBuilder();
            for(int i = 9; i >= 0; i--){
                int common = Math.min(countx[i], county[i]);
                for(int k = 0; k < common; k++){
                    sb.append(i);
                }
            }

            // 공통 숫자 없음
            if (sb.length() == 0) return "-1";
            // 공통 숫자가 모두 0
            if (sb.charAt(0) == '0') return "0";

            return sb.toString();
        }
    }
}
