package 이코테_자바.chapter8;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class 효율적인_화폐구성 {
    public static void main(String[] args) throws IOException {
        // 입력
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int N = Integer.parseInt(st.nextToken());
        int M = Integer.parseInt(st.nextToken());

        int[] arr = new int[N];
        for(int i = 0; i < N; i++){
            arr[i] = Integer.parseInt(br.readLine());
        }

        // DP 테이블
        int[] dp = new int [10001];
        Arrays.fill(dp, 10001); // 기본값 초기화

        dp[0] = 0; // 반드시 필요함 0원을 만드는 데 필요한 화폐 개수 = 0개
        for(int i = 0; i < N; i++){
            for(int j = arr[i]; j < M+1; j++){
                if (dp[j - arr[i]] != 10001){
                    dp[j] = Math.min(dp[j], dp[j - arr[i]] + 1);
                }
            }
        }

        if (dp[M] == 10001){
            System.out.println(-1);
        } else {
            System.out.println(dp[M]);
        }

    }
}
