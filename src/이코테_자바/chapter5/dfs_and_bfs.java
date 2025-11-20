package 이코테_자바.chapter5;

import java.util.*;
import java.io.*;


public class dfs_and_bfs {
    static ArrayList<Integer>[] graph;
    static boolean[] visited;
    static int N, M;

    public static void main(String args[]) throws IOException{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());

        graph = new ArrayList[N+1];
        for(int i = 1; i <= N; i++){
            graph[i] = new ArrayList<>();
        }

        for (int i = 0; i < M; i++){
            st = new StringTokenizer(br.readLine());
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            graph[a].add(b);
            graph[b].add(a);
        }

        // 정렬
        for(int i = 1; i <= N; i++){
            Collections.sort(graph[i]);
        }

        visited = new boolean[N+1];
        System.out.print("DFS: ");
        dfs(1);
        System.out.println();

        visited = new boolean[N+1];
        System.out.print("BFS: ");
        bfs(1);
        System.out.println();
    }

    static void dfs(int v){
        visited[v] = true;
        System.out.print(v+ " ");
        for(int next: graph[v]){
            if (!visited[next]){
                dfs(next);
            }
        }
    }

    static void bfs(int start){
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(start);
        visited[start] = true;

        while (!queue.isEmpty()){
            int v = queue.poll();
            System.out.print(v + " ");

            for(int next: graph[v]){
                if(!visited[next]){
                    queue.offer(next);
                    visited[next] = true;
                }

            }
        }


    }
}
