package programmers.lv2;
import java.util.*;

public class 정렬_가장큰수 {

    class Solution {
        public String solution(int[] numbers) {

            String[] arr = new String[numbers.length];
            for(int i = 0; i < numbers.length; i++){
                arr[i] = String.valueOf(numbers[i]);
            }

            Arrays.sort(arr, (a, b) ->  (b+a).compareTo(a+b));

            if (arr[0].equals("0")) return "0";

            StringBuilder sb = new StringBuilder();
            for(String s: arr) sb.append(s);

            return sb.toString();
        }
    }

}
