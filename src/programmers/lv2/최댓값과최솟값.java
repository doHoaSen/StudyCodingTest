package programmers.lv2;
import java.util.*;

public class 최댓값과최솟값 {
    class Solution {
        public String solution(String s) {
            String[] arr = s.split(" ");

            int min = Integer.MAX_VALUE;
            int max = Integer.MIN_VALUE;

            for(String str: arr){
                int num = Integer.parseInt(str);
                min = Math.min(min, num);
                max = Math.max(max, num);
            }

            return min + " " + max;
        }


        public String solution2(String s){
            String[] arr = s.split(" ");
            int[] nums = new int[arr.length];

            for(int i  = 0; i < arr.length; i++){
                nums[i] = Integer.parseInt(arr[i]);
            }

            Arrays.sort(nums);

            return nums[0] + " " + nums[nums.length - 1];
        }
    }
}
