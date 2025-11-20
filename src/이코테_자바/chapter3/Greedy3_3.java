package 이코테_자바.chapter3;

import java.io.*;
import java.util.*;

public class Greedy3_3 {
    public static void main(String args[]) throws IOException{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());

        int result = 0;
        for (int i = 0; i < n; i++){
            st = new StringTokenizer(br.readLine());
            int minVal = Integer.MAX_VALUE;

            // 현재 행의 최솟값 찾기
            for (int j = 0; j < m; j++){
                int value = Integer.parseInt(st.nextToken());
                minVal = Math.min(minVal, value);
            }

            // 각 행의 최솟값 중 최댓값 구하기
            result = Math.max(minVal, result);
        }
        System.out.println(result);
    }
}
