package 이코테_자바.chapter9;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

public class 다익스트라_개선9_2 {
    static class Node implements Comparable<Node>{
        int to;
        int cost;

        Node(int to, int cost){
            this.to = to;
            this.cost = cost;
        }

        @Override
                public int compareTo(Node o){
            return this.cost - o.cost;
        }

        // 노드 정렬 기준 제공하지 않으면 에러 발생
        // 왜 정렬 기준을 제공해야 함?
//        자바의 PriorityQueue 설명을 보면
//        “Elements are ordered according to their natural ordering,
//        or by a Comparator provided at queue construction time.”
//        정렬을 해주긴 하는데 “무엇을 기준으로” 정렬할지는 모른다
//        힙은 값의 크기 개념이 필요

        // 힙이 자동으로 알 수 있는 경우
        // 기본 타입 or Comparable 구현 객체

    }

    static final int INF =  Integer.MAX_VALUE;
    static int N, M, start;
    static ArrayList<Node>[] graph;
    static int[] distance;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());

        start = Integer.parseInt(br.readLine());

        graph = new ArrayList[N+1];
        for(int i = 1; i <= N; i++){
            graph[i] = new ArrayList<>();
        }

        distance = new int[N+1];
        Arrays.fill(distance, INF);

        // 간선 입력
        for(int i = 0; i < M; i++){
            st = new StringTokenizer(br.readLine());
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            int c = Integer.parseInt(st.nextToken());

            graph[a].add(new Node(b, c));
        }

        dijkstra(start);

        // 결과 출력
        for(int i = 1; i <= N; i++){
            if (distance[i] == INF){
                System.out.println("INFINITY");
            } else {
                System.out.println(distance[i]);
            }
        }

    }

    // 개선된 다익스트라  알고리즘
     static void dijkstra(int start){
         PriorityQueue<Node> pq = new PriorityQueue<>();
         // Node클래스에서 Comparable 사용하지 않는다면
         // Comparator 사용해서 외부에서 주는 규칙 적용할 수도
         // PriorityQueue<Node> pq =  new PriorityQueue<>(Comparator.comparingInt(n -> n.cost));
         pq.offer(new Node(start, 0));
         distance[start] = 0;

         while(!pq.isEmpty()){
             Node cur = pq.poll();
             int now = cur.to;
             int dist = cur.cost;

             if (distance[now] < dist) continue;

             for(Node next: graph[now]){
                 int cost = distance[now] + next.cost;
                 if (cost < distance[next.to]){
                     distance[next.to] = cost;
                     pq.offer(new Node(next.to, cost));
                 }
             }
         }
     }
}

// 시간복잡도: O(ElogV)

// Comparable vs. Comparator
// Comparable = “내가 나를 어떻게 비교할지”
// Comparator = “남이 나를 어떻게 비교할지”

// Comparable
// 클래스 내부에 정의, 기본 정렬 기준, implements Comparable<T>
//class Student implements Comparable<Student> {
//    String name;
//    int score;
//
//    @Override
//    public int compareTo(Student o) {
//        return this.score - o.score; // 점수 오름차순
//    }
//}

// Comparator
// 클래스 외부에서 정의, 정렬 기준을 바꿀 수 있음, Comparator<T>
//Comparator<Student> scoreDesc = new Comparator<>() {
//    @Override
//    public int compare(Student a, Student b) {
//        return b.score - a.score; // 점수 내림차순
//    }
//};
//또는
//Comparator<Student> scoreDesc =
//        (a, b) -> b.score - a.score;
