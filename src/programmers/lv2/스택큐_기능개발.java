package programmers.lv2;
import java.util.*;

public class 스택큐_기능개발 {

    class Solution {
        public int[] solution(int[] progresses, int[] speeds) {
            Queue<Integer> q = new LinkedList<>();
            List<Integer> answerlist = new ArrayList<>();

            for(int i = 0; i < progresses.length; i++){
                double remain = (double)(100 - progresses[i]) / speeds[i];
                int date = (int)Math.ceil(remain);

                if (!q.isEmpty() && q.peek() < date) {
                    answerlist.add(q.size());
                    q.clear();
                }
                q.offer(date);
            }

            answerlist.add(q.size());

            int[] answer = new int[answerlist.size()];
            for (int i = 0; i < answer.length; i++) {
                answer[i] = answerlist.get(i);
            }

            return answer;
        }
    }
}
