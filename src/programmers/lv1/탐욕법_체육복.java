package programmers.lv1;
import java.util.*;

public class 탐욕법_체육복 {

    class Solution {
        public int solution(int n, int[] lost, int[] reserve) {
            int answer = 0;

            // 정렬
            Arrays.sort(lost);
            Arrays.sort(reserve);

            // lost와 reserve 겹치는 학생 제거
            Set<Integer> lostSet = new HashSet<>();
            Set<Integer> reserveSet = new HashSet<>();

            for(int l: lost) lostSet.add(l);
            for(int r: reserve) reserveSet.add(r);

            Set<Integer> both = new HashSet<>(lostSet);
            both.retainAll(reserveSet);

            for(int b: both){
                lostSet.remove(b);
                reserveSet.remove(b);
            }

            // 빌려줄 수 있는지 체크
            for(int r: reserveSet){
                // 왼쪽 숫자
                if(lostSet.contains(r-1)){
                    lostSet.remove(r-1);
                } else if (lostSet.contains(r+1)){
                    lostSet.remove(r+1);
                }
            }
            return n - lostSet.size();
        }
    }
}
