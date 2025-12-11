package programmers.lv1;
import java.util.*;

public class 문자열_내마음대로_정렬하기 {


    class Solution {
        public String[] solution(String[] strings, int n) {

            Arrays.sort(strings, new Comparator<String>(){
                @Override
                public int compare(String o1, String o2){
                    if(o1.charAt(n) < o2.charAt(n)) {
                        return -1;
                    } else if (o1.charAt(n) == o2.charAt(n)){
                        return o1.compareTo(o2);
                    } else if (o1.charAt(n) > o2.charAt(n)){
                        return 1;
                    } else {
                        return 0;
                    }
                }
            });
            return strings;
        }
    }

    class Solution2 {
        public String[] solution(String[] strings, int n) {
            ArrayList<String> arr = new ArrayList<>();
            for(int i = 0; i < strings.length; i++){
                arr.add(""+strings[i].charAt(n)+strings[i]);
            }

            Collections.sort(arr);
            String[] answer = new String[arr.size()];
            for(int i = 0; i < arr.size(); i++){
                answer[i] = arr.get(i).substring(1, arr.get(i).length());
            }

            return answer;
        }
    }
}
