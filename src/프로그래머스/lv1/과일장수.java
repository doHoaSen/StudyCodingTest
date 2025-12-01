package 프로그래머스.lv1;

import java.util.*;
public class 과일장수 {

    class Solution {
        public int solution(int k, int m, int[] score) {
            int answer = 0;
            // 상자 개수
            int boxes = score.length / m;
            // score 정렬
            Arrays.sort(score);

            for(int i = score.length; i >= m; i -= m){
                answer += score[i-m]*m;
            }
            return answer;
        }
    }

    class Solution2 {
        public int solution(int k, int m, int[] score) {
            int answer = 0;

            // 1~k 점수이므로 빈도 수 배열 생성
            int[] freq = new int[k + 1];

            // 점수 빈도 세기
            for (int s : score) {
                freq[s]++;
            }

            int count = 0; // 현재 상자에 들어간 사과 개수

            // k(최대점수)부터 1까지 내려가며 처리
            for (int i = k; i >= 1; i--) {
                while (freq[i] > 0) {
                    freq[i]--;
                    count++;

                    // 상자가 꽉 차면 계산
                    if (count == m) {
                        answer += i * m; // i는 현재 묶음에서 가장 낮은 점수
                        count = 0;        // 새 상자 시작
                    }
                }
            }

            return answer;
        }
    }

}
