package programmers.lv1;
import java.util.*;

public class 달리기경주 {

    class Solution {
        public String[] solution(String[] players, String[] callings) {

            Map<String, Integer> map = new HashMap<>();

            for(int i = 0; i < players.length; i++){
                map.put(players[i], i);
            }

            for(String name: callings){
                int cur = map.get(name);
                int front = cur - 1;

                if (front >= 0){
                    String frontPlayer = players[front];
                    // swap
                    players[front] = name;
                    players[cur] = frontPlayer;
                    map.put(name, front);
                    map.put(frontPlayer, cur);
                }



            }
            return players;
        }
    }
}
