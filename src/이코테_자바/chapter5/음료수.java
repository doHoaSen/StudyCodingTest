package 이코테_자바.chapter5;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

// 덩어리 -> dfs
public class 음료수 {
    static int N, M;
    static boolean[][] visited;
    static int[][] map;
    public static void main(String[] args) throws IOException {
        BufferedReader br= new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());

        map = new int[N][M];
        visited = new boolean[N][M];

        // 2차원 배열 입력
        for (int i = 0; i < N; i++){
            String line = br.readLine();
            for(int j = 0; j < M; j++){
                map[i][j] = line.charAt(j) - '0';
            }
        }

        int cnt = 0;
        // 칸 탐색
        for(int i = 0; i < N; i++){
            for (int j = 0; j < M; j++){
                if (dfs(i, j)){
                    cnt++;
                }
            }
        }
        System.out.println(cnt);


    }

    static boolean dfs(int x, int y){
        if (x < 0 || x >= N || y < 0 || y >= M){
            return false;
        }
        if (!visited[x][y] && map[x][y] == 0){
            visited[x][y] = true;

            // 상하좌우 탐색
            dfs(x-1, y);
            dfs(x+1, y);
            dfs(x, y-1);
            dfs(x, y+1);

            return true; // 새로운 덩어리 발견
        }
        return false;
    }
}
