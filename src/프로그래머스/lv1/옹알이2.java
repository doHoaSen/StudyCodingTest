package 프로그래머스.lv1;

public class 옹알이2 {
    class Solution {
        public int solution(String[] babbling) {
            int answer = 0;
            String[] words = {"aya", "ye", "woo", "ma"};

            for(String b: babbling){

                // 연속x -> 왼쪽부터 발음 확인, 기억하기
                String prev = "";
                boolean ok = true;

                while(!b.isEmpty()){
                    boolean matched = false;

                    for(String w:words){
                        if(b.startsWith(w)){
                            if(w.equals(prev)){
                                ok = false;
                                break;
                            }
                            prev = w;
                            b = b.substring(w.length());
                            matched = true;
                            break;
                        }
                    }
                    if (!matched){
                        ok = false;
                        break;
                    }
                }


                if(ok) answer++;

            }
            return answer;

        }
    }

    class Solution2 {
        public int solution(String[] babbling) {
            int answer = 0;
            for(int i = 0; i < babbling.length; i++){
                if(babbling[i].contains("ayaaya") || babbling[i].contains("yeye") || babbling[i].contains("woowoo") || babbling[i].contains("mama")) {
                    continue;
                }
                babbling[i] = babbling[i].replace("aya", " ");
                babbling[i] = babbling[i].replace("ye", " ");
                babbling[i] = babbling[i].replace("woo", " ");
                babbling[i] = babbling[i].replace("ma", " ");
                babbling[i] = babbling[i].replace(" ", "");

                if (babbling[i].length() == 0) answer++;
            }
            return answer;

        }
    }

}
