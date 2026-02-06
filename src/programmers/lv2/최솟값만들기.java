package programmers.lv2;
import java.util.*;

public class 최솟값만들기 {

    class Solution {
        public int solution(int []A, int []B) {
            // 1 2 4 / 4 4 5  => 5+8+16
            Arrays.sort(A);
            Arrays.sort(B);

            int total = 0;
            for(int i = 0; i < A.length; i++){

                total += A[i] * B[B.length - 1 - i];
            }

            return total;
        }
    }
}
