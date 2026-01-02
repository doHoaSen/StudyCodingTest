package programmers.lv2;
import java.util.*;

public class 정렬_HIndex {

    class Solution {
        public int solution(int[] citations) {

            Arrays.sort(citations);
            int h = 0;
            for(int i = 0; i < citations.length; i++){
                // i번째 논문의 인용 수가 (i+1) 이상
                int candidate = citations.length - i;
                if (citations[i] >= candidate){
                    h = candidate;
                    break;
                }
            }
            return h;
        }
    }
}
