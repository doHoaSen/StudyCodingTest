package programmers.lv2;
import java.util.*;

public class 짝지어제거하기 {

    class Solution {
        public int solution(String s){
            // 스택 사용
            Stack<Character> stack = new Stack<>();

            for(char c: s.toCharArray()){
                if(!stack.isEmpty() && stack.peek() == c){
                    stack.pop();
                } else {
                    stack.push(c);
                }
            }

            return stack.isEmpty() ? 1 : 0;
        }
    }
}
