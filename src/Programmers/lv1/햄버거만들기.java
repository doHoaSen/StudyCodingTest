package Programmers.lv1;
import java.util.*;

public class 햄버거만들기 {
    class Solution {
        public int solution(int[] ingredient) {
            Stack<Integer> stack = new Stack<>();
            int count = 0;

            for (int ing : ingredient) {
                stack.push(ing);

                if (stack.size() >= 4) {
                    int size = stack.size();
                    // 끝에서 1,2,3,1 순으로 되어 있는지 체크
                    if (stack.get(size - 4) == 1 &&
                            stack.get(size - 3) == 2 &&
                            stack.get(size - 2) == 3 &&
                            stack.get(size - 1) == 1) {

                        // 햄버거 완성 → pop 4번
                        stack.pop();
                        stack.pop();
                        stack.pop();
                        stack.pop();
                        count++;
                    }
                }
            }
            return count;
        }
    }

}
