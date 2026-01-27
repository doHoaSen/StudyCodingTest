package programmers.lv1;

public class 택배상자꺼내기 {
    class Solution {
        public int solution(int n, int w, int num) {
            int height = (n / w) + 1;
            int[][] arr = new int[height][w];
            int cnt = 1;
            // num의 위치 저장
            int col = 0; int row = 0;

            // 쌓기
            for(int i = 0; i <= height; i++){
                // i = 0이거나 짝수면 왼 -> 오
                if(i % 2 == 0){
                    for(int j = 0; j < w; j++){
                        if (cnt > n) break;
                        if (cnt == num){
                            col = i;
                            row = j;
                        }
                        arr[i][j] = cnt++;
                    }
                } else {
                    // i가 홀수면 오 -> 왼
                    for(int j = w-1; j >= 0; j--){
                        if (cnt > n) break;
                        if (cnt == num){
                            col = i;
                            row = j;
                        }
                        arr[i][j] = cnt++;
                    }
                }


            }

            // 꺼내기
            int answer = 0;
            for(int i = col; i < height; i++){
                if (arr[i][row] != 0){
                    answer++;
                }
            }

            return answer;
        }
    }
}
