package 이코테_자바.chapter5;

import java.util.ArrayList;

public class dfs5_8 {
    static ArrayList<Integer>[] graph;
    static boolean[] visited;

    public static void main (String args[]){
        graph = new ArrayList[9];
        visited = new boolean[9];

        for (int i = 0; i < 9; i++){
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

        dfs(1); // 시작노드 = 1
    }

    public static void dfs(int v){
        visited[v] = true;
        System.out.print(v + " ");

        for(int next: graph[v]){
            if (!visited[next]){
                dfs(next);
            }
        }
    }
}
