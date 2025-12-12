package 이코테_자바.chapter6;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class 두배열의원소교체 {
    public static void main(String[] args) throws IOException {
        int N, K;
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        K = Integer.parseInt(st.nextToken());

        // 배열 선언
        int[] A = new int[N];
        int[] B = new int[N];

        st = new StringTokenizer(br.readLine());
        for(int i = 0; i < N; i++){
            A[i] = Integer.parseInt(st.nextToken());
        }

        st = new StringTokenizer(br.readLine());
        for(int i = 0; i < N; i++){
            B[i] = Integer.parseInt(st.nextToken());
        }

        // 배열 A의 가장 작은 값과 배열 B의 가장 큰 값 교환
        Arrays.sort(A); // 1 2 3 4 5
        Arrays.sort(B); // 5 5 5 6 6

        // 즉, A의 가장 작은 값이 배열 b의 가장 큰 값보다 작을 때만 교환a
        for(int i = 0; i < K; i++){
            if(A[i] < B[N-1-i]){
                int temp = A[i];
                A[i] = B[N-1 - i];
                B[N-1-i] = temp;
            } else {
                break;
            }
        }

        int result = 0;
        for(int i: A){
            result += i;
        }

        System.out.println(result);
    }
}
