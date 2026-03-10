package programmers.lv2;
import java.util.*;

public class 구명보트 {
    class Solution {
        public int solution(int[] people, int limit) {
            // 정렬
            Arrays.sort(people);

            // 반복문
            int left = 0;
            int right = people.length - 1;
            int cnt = 0;

            // 무거운 사람부터 처리
            while (left <= right){
                if(people[left] + people[right] <= limit){
                    left++;
                }
                right--;
                cnt++;
            }
            return cnt;
        }
    }
}
