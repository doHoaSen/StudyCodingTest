package 이코테_자바.chapter3;

import java.io.*;
import java.util.*;

public class Greedy3_4 {
    public static void main(String args[]) throws IOException{
        int cnt = 0;
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        
        // n이 k의 배수가 될 때까지 1을 빼고
        // 계속 k로 나누기
        while (n >= k){
            while (n % k != 0){
                n -= 1;
                cnt++;
            }
            n /= k;
            cnt++;
        }

        while (n > 1){
            n -= 1;
            cnt++;
        }

        System.out.println(cnt);
    }
}
