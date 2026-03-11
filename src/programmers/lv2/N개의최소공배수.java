package programmers.lv2;

public class N개의최소공배수 {
    class Solution {
        public int solution(int[] arr) {
            int lcm = arr[0];
            for(int i = 1; i < arr.length; i++){
                lcm = lcm(lcm, arr[i]);
            }
            return lcm;
        }

        public int lcm(int x, int y){
            return x * y / gcd(x, y);
        }

        public int gcd(int x, int y){
            while (y != 0){
                int temp = x % y;
                x = y;
                y = temp;
            }
            return x;
        }
    }
}
