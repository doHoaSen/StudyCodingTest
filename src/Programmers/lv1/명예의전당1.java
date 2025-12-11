package programmers.lv1;
import java.util.*;

public class 명예의전당1 {

    class Solution {
        public int[] solution(int k, int[] score) {
            int[] answer = new int[score.length];
            ArrayList<Integer> list = new ArrayList<>();

            for(int i = 0; i < score.length; i++){
                list.add(score[i]);
                list.sort(Comparator.naturalOrder());
                if (list.size() > k){
                    list.remove(0);
                }
                answer[i] = list.get(0);
            }
            return answer;
        }
    }

    class Solution2 {
        public int[] solution(int k, int[] score) {
            int[] answer = new int[score.length];
            PriorityQueue<Integer> queue = new PriorityQueue<>();

            for(int i = 0; i < score.length; i++){
                queue.add(score[i]);
                if (queue.size() > k)  queue.poll();
                answer[i] = queue.peek();
            }
            return answer;
        }
    }
}
