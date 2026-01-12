package 이코테_자바.chapter9;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.StringTokenizer;

public class 다익스트라_간단9_1 {
    static class Node {
        int to;
        int cost;

        Node(int to, int cost) {
            this.to = to;
            this.cost = cost;
        }
    }

    static int N, M, start;
    static ArrayList<Node>[] graph;
    static boolean[] visited;
    static int[] distance;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());

        // 시작 노드 번호 입력받기
        start = Integer.parseInt(br.readLine());

        // 각 노드에 연결되어 있는 노드에 대한 정보를 담는 리스트 만들기
        graph = new ArrayList[N + 1];
        for (int i = 1; i < N + 1; i++) {
            graph[i] = new ArrayList<>();
        }

        visited = new boolean[N + 1];
        distance = new int[N + 1];
        Arrays.fill(distance, Integer.MAX_VALUE);

        // 모든 간선 정보 입력받기
        for (int i = 0; i < M; i++) {
            st = new StringTokenizer(br.readLine());
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            int c = Integer.parseInt(st.nextToken());
            // a번 노드에서 b번 노드로 가는 비용이 c라는 의미
            graph[a].add(new Node(b, c));
        }

        dijkstra(start);

        // 결과 출력
        for(int i = 1; i <= N; i++){
            if (distance[i] == Integer.MAX_VALUE){
                System.out.println("INFINITY");
            } else {
                System.out.println(distance[i]);
            }
        }


    }

    // 다익스트라 알고리즘
    static void dijkstra(int start){
        // 시작 노드에 대해 초기화
        distance[start] = 0;

        // 시작 노드와 연결된 노드 초기화
        for(Node node: graph[start]){
            distance[node.to] = node.cost;
        }
        visited[start] = true;

        // 시작 노드 제외한 N-1개 노드 처리
        for(int i = 0; i < N-1; i++){
            int now = get_smallest_node();
            visited[now] = true;

            for(Node node: graph[now]){
                int cost = distance[now] + node.cost;
                if (cost < distance[node.to]){
                    distance[node.to] = cost;
                }
            }
        }

    }


    // 방문하지 않은 노드 중에서 가장 최단 거리가 짧은 노드의 번호 반환
    static int get_smallest_node(){
        int minValue  = Integer.MAX_VALUE;
        int index = 0; // 가장 최단 거리가 짧은 노드(인덱스)
        for(int i = 1; i < N+1; i++){
            if (distance[i] < minValue && !visited[i]){
                minValue = distance[i];
                index = i;
            }
        }
        return index;
    }
}

// 시간복잡도: O(V^2)
// V: 노드의 개수