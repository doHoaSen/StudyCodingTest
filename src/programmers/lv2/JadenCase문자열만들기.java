package programmers.lv2;

public class JadenCase문자열만들기 {
    class Solution {
        public String solution(String s) {
            // 첫 문자: 숫자 -> 나머지 소문자 / 영어 -> 대문자
            // 나머지: 영어면 소문자 / 나머지 그대로

            StringBuilder sb = new StringBuilder();
            boolean isStart = true;

            for(char c: s.toCharArray()){
                if (c == ' '){
                    sb.append(c);
                    isStart = true;
                } else {
                    if (isStart){
                        sb.append(Character.toUpperCase(c));
                        isStart = false;
                    } else {
                        sb.append(Character.toLowerCase(c));
                    }
                }
            }

            return sb.toString();
        }
    }
}
