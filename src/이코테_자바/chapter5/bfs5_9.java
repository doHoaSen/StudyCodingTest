package 이코테_자바.chapter5;

import java.util.*;

public class bfs5_9 {
    static ArrayList<Integer>[] graph;
    static boolean[] visited;

    public static void main(String args[]){
        graph = new ArrayList[9];
        visited = new boolean[9];

        for (int i = 0; i < 9; i++) {
            graph[i] = new ArrayList<>();
        }

        graph[1].add(2); graph[1].add(3); graph[1].add(8);
        graph[2].add(1); graph[2].add(7);
        graph[3].add(1); graph[3].add(4); graph[3].add(5);
        graph[4].add(3); graph[4].add(5);
        graph[5].add(3); graph[5].add(4);
        graph[6].add(7);
        graph[7].add(2); graph[7].add(6); graph[7].add(8);
        graph[8].add(1); graph[8].add(7);

        bfs(1);
    }

    public static void bfs(int start){
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(start);
        visited[start] = true;

        while(!queue.isEmpty()){
            int v = queue.poll();
            System.out.print(v + " ");

            for(int next : graph[v]){
                if (!visited[next]){
                    queue.offer(next);
                    visited[next] = true;
                }
            }
        }
    }
}
