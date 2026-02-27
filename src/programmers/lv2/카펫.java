package programmers.lv2;

public class 카펫 {
    class Solution {
        public int[] solution(int brown, int yellow) {
            int total = brown + yellow;
            for(int h = 1; h * h <= yellow; h++){
                if (yellow % h == 0){
                    int w = yellow / h;

                    if ((w + 2) * (h + 2) == total){
                        return new int[]{w+2, h+2};
                    }
                }
            }
            return null;
        }
    }
}
