package programmers.lv1;
import java.util.*;

public class 크레인_인형뽑기_게임 {

    class Solution {
        public int solution(int[][] board, int[] moves) {
            Stack<Integer> basket = new Stack<>();
            int answer = 0;

            for(int move: moves){
                int col = move-1;
                // 뽑히는 인형 -> 행이 0이 아닌 시점
                for(int row = 0; row < board.length; row++){
                    if(board[row][col] != 0){
                        int picked = board[row][col];
                        board[row][col] = 0;

                        // 바구니 안 인형과 비교
                        if (!basket.isEmpty() && basket.peek() == picked){
                            basket.pop();
                            answer += 2;
                        } else {
                            basket.push(picked);
                        }
                        break;
                    }
                }
            }

            return answer;
        }
    }
}
