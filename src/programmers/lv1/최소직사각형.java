package programmers.lv1;

import java.util.*;
public class 최소직사각형 {
    class Solution {
        public int solution(int[][] sizes) {
            int answer = 0;
            // 그리디?
            // 회전 가능 -> 정렬 후 1열의 최댓값 * 2열의 최댓값
            int maxW = 0;
            int maxH = 0;

            for(int[] card: sizes){
                int w = Math.max(card[0], card[1]);
                int h = Math.min(card[0], card[1]);

                maxW = Math.max(maxW, w);
                maxH = Math.max(maxH, h);
            }

            return maxW * maxH;
        }
    }
}
