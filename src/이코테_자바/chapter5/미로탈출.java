package 이코테_자바.chapter5;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class 미로탈출 {
    static int N;
    static int M;
    static int[][] map;
    // 좌, 우, 하, 상
    static int[] dx = {-1, 1, 0, 0};
    static int[] dy = {0, 0, -1, 1};


    public static void main(String args[]) throws IOException {
        // 입력
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());
        map = new int[N][M];
        for(int i = 0; i < N; i++){
            String line = br.readLine();
            for (int j = 0; j < M; j++) {
                map[i][j] = line.charAt(j) - '0';
            }
        }

        // BFS


        int result = bfs(0, 0);
        System.out.println(result);

    }

    static int bfs(int x, int y){
        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{x, y});

        while(!queue.isEmpty()){
            int [] now = queue.poll();
            int cx = now[0];
            int cy = now[1];

            // 4가지 방향 이동
            for(int i = 0; i < 4; i++){
                int nx = cx + dx[i];
                int ny = cy + dy[i];

                if (nx < 0 || nx >= N || ny < 0 || ny >= M){
                    continue;
                }

                if (map[nx][ny] == 1){
                    map[nx][ny] = map[cx][cy] + 1; // 거리 증가
                    queue.offer(new int[]{nx, ny});
                }
            }
        }
        return map[N-1][M-1];
    }
}
