package programmers.lv1;
import java.util.*;

public class 스택큐_같은숫자는싫어 {

    public class Solution {
        public int[] solution(int []arr) {
            Stack<Integer> stack = new Stack<>();
            stack.push(arr[0]);
            for(int i = 1; i < arr.length; i++){
                if (stack.peek() == arr[i]){
                    continue;
                }
                stack.push(arr[i]);
            }

            int[] answer = new int[stack.size()];
            for(int i = stack.size(); i > 0; i--){
                answer[i-1] = stack.pop();
            }

            return answer;
        }

        public int[] solution2(int[] arr){
            Stack<Integer> stack = new Stack<>();
            for(int n: arr){
                if(stack.size() == 0 | stack.peek() != n){
                    stack.push(n);
                }
            }
            int[] answer = new int[stack.size()];
            for(int i = stack.size(); i > 0; i--){
                answer[i-1] = stack.pop();
            }

            return answer;
        }

    }
}
