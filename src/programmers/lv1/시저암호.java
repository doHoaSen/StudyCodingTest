package programmers.lv1;

public class 시저암호 {
    class Solution {
        public String solution(String s, int n) {
            StringBuilder answer = new StringBuilder();
            for(char ch : s.toCharArray()){
                if (ch == ' ') {
                    answer.append(ch);
                    continue;
                } else {
                    char base = Character.isUpperCase(ch) ? 'A': 'a';
                    ch = (char)((ch - base + n) % 26 + base);
                    answer.append(ch);
                }
            }
            return answer.toString();
        }
    }
}
