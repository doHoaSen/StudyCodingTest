package programmers.lv1;
import java.util.Arrays;

public class 정렬_K번째수 {

    class Solution {
        public int[] solution(int[] array, int[][] commands) {
            int[] answer = new int[commands.length];
            for(int i = 0; i < commands.length; i++){
                int[] command = commands[i];
                int[] arr = Arrays.copyOfRange(array, command[0]-1, command[1]);
                Arrays.sort(arr);
                answer[i] = arr[command[2]-1];
            }
            return answer;
        }
    }
}
