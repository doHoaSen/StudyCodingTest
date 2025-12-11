package Programmers.lv1;
import java.util.*;

public class 두개_뽑아서_더하기 {

    class Solution {
        public int[] solution(int[] numbers) {
            HashSet<Integer> set = new HashSet<>();

            for(int i = 0; i < numbers.length; i++){
                for(int j = i+1; j < numbers.length; j++){
                    set.add(numbers[i]+numbers[j]);
                }
            }

            int idx = 0;
            int[] answer = new int[set.size()];
            for(int num: set){
                answer[idx++] = num;
            }

            Arrays.sort(answer);

            return answer;
        }
    }

    class Solution2 {
        public int[] solution(int[] numbers) {
            TreeSet<Integer> set = new TreeSet<>();

            for (int i = 0; i < numbers.length; i++) {
                for (int j = i + 1; j < numbers.length; j++) {
                    set.add(numbers[i] + numbers[j]);
                }
            }

            // TreeSet → 정렬된 int[]
            return set.stream().mapToInt(Integer::intValue).toArray();
        }
    }
}
