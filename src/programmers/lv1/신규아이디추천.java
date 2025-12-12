package programmers.lv1;

public class 신규아이디추천 {
    class Solution {
        public String solution(String new_id) {
            String str = new_id.toLowerCase();
            str = str.replaceAll("[^a-z0-9-_.]", "");
            str = str.replaceAll("\\.+", ".");
            if (str.startsWith(".")) str = str.substring(1);
            if (str.endsWith(".")) str = str.substring(0, str.length()-1);
            if (str.length() == 0) str = "a";
            if (str.length() >= 16){
                str = str.substring(0, 15);
                if (str.endsWith(".")) str = str.substring(0, str.length()-1);
            }
            while(str.length() < 3){
                str += str.charAt(str.length()-1);
            }
            return str;
        }
    }
}
