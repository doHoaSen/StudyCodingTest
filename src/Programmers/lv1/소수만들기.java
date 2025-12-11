package programmers.lv1;

public class 소수만들기 {
    class Solution {

        public int solution(int[] nums) {
            int answer = 0;
            boolean flag = true;

            for(int i = 0; i < nums.length; i++){
                for(int j = i+1; j < nums.length; j++){
                    for(int k = j+1; k < nums.length; k++){
                        int num = nums[i] + nums[j] + nums[k];
                        if (num >= 2){
                            flag = sosu(num);
                        }
                        if(flag == true) answer++;
                    }
                }
            }
            return answer;
        }


        // 소수: 약수가 1과 자신만 존재함
        public boolean sosu(int number){
            boolean flag = true;
            if (number == 2) {
                return true;
            }
            for(int i = 2; i < number; i++){
                if (number % i == 0){
                    flag = false;
                    break;
                }
            }

            return flag;
        }
    }
}
