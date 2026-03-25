package programmers.lv2;
import java.util.*;

public class 연속부분수열합의개수 {

    class Solution {
        public int solution(int[] elements) {
            Set<Integer> set = new HashSet<>();
            int start = 1;
            while(start <= elements.length){
                for(int i = 0; i < elements.length; i++){
                    int sum = 0;
                    for(int j = i; j < i+start; j++){
                        sum += elements[j % elements.length];
                    }
                    set.add(sum);
                }
                start++;
            }
            return set.size();
        }
    }
}
