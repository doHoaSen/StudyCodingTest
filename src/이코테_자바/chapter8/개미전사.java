package 이코테_자바.chapter8;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class 개미전사 {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] arr = new int [n];
        for(int i = 0; i < n; i++){
            arr[i] = Integer.parseInt(st.nextToken());
        }

        int[] d = new int [100];
        d[0] = 0;
        d[1] = Math.max(arr[0], arr[1]);
        for(int i = 2; i < n+1; i++){
            d[i] = Math.max(d[i-1], d[i-2]+arr[i-1]);
        }

        System.out.println(d[n]);
    }
}
