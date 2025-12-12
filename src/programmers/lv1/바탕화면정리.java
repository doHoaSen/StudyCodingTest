package programmers.lv1;

public class 바탕화면정리 {
    class Solution {
        public int[] solution(String[] wallpaper) {
            int[] answer = {};
            int minRow = Integer.MAX_VALUE;
            int maxRow = Integer.MIN_VALUE;
            int minCol = Integer.MAX_VALUE;
            int maxCol = Integer.MIN_VALUE;

            for(int r = 0; r < wallpaper.length; r++){
                for(int c = 0; c < wallpaper[r].length(); c++){
                    if(wallpaper[r].charAt(c) == '#'){
                        minRow = Math.min(minRow, r);
                        maxRow = Math.max(maxRow, r);

                        minCol = Math.min(minCol, c);
                        maxCol = Math.max(maxCol, c);
                    }
                }
            }
            return new int[] {minRow, minCol, maxRow+1, maxCol+1};
        }
    }
}
