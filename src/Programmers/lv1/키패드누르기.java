package Programmers.lv1;

public class 키패드누르기 {
    class Solution {
        public String solution(int[] numbers, String hand) {
            String answer = "";
            StringBuilder sb = new StringBuilder();
            int left = 10;
            int right = 12;

            for(int num: numbers){
                //1, 4, 7은 왼손
                if (num == 1 || num == 4 || num == 7){
                    sb.append("L");
                    left = num;
                }
                // 3, 6, 9는 오른손
                else if (num == 3 || num == 6 || num == 9){
                    sb.append("R");
                    right = num;
                }
                // 2, 5, 8, 0 거리 계산
                else {
                    if (num == 0) num = 11;
                    int leftDist = getDist(left, num);
                    int rightDist = getDist(right, num);

                    if (leftDist < rightDist){
                        sb.append("L");
                        left = num;
                    } else if (leftDist > rightDist){
                        sb.append("R");
                        right = num;
                    } else {
                        if (hand.equals("right")){
                            sb.append("R");
                            right = num;
                        } else {
                            sb.append("L");
                            left = num;
                        }
                    }
                }

            }
            return sb.toString();
        }

        int getDist2(int from, int to){
            int fx = (from - 1) / 3;
            int fy = (from - 1) % 3;
            int tx = (to - 1) / 3;
            int ty = (to - 1) % 3;

            return Math.abs(fx - tx) + Math.abs(fy - ty);
        }

        private int getDist(int from, int to) {
            int diff = Math.abs(from - to);
            return diff / 3 + diff % 3;
        }


    }
}
