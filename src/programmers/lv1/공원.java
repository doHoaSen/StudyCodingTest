package programmers.lv1;
import java.util.*;

public class 공원 {

    class Solution {
        public int solution(int[] mats, String[][] park) {
            int answer = 0;
            int h = park.length;
            int w = park[0].length;

            Arrays.sort(mats);
            // 큰 종류의 매트부터 들어갈 수 있는지 검사
            for (int idx = mats.length - 1; idx >= 0; idx--) {
                int k = mats[idx];
                for(int r = 0; r + k <= h; r++){
                    for(int c = 0; c + k <= w; c++){
                        if(canPlace(park, r, c, k)){
                            return k;
                        }
                    }
                }
            }
            return -1;
        }

        private boolean canPlace(String[][] park, int r, int c, int k){
            for(int i = r; i < r+k; i++){
                for(int j = c; j < c+k; j++){
                    if (!park[i][j].equals("-1")){
                        return false;
                    }
                }
            }
            return true;
        }
    }
}
