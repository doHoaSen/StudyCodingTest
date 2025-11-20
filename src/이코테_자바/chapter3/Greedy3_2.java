package 이코테_자바.chapter3;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class Greedy3_2 {
    public static void main(String args[]) throws IOException {
        // n, m, k를 공백으로 구분하여 입력하기
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());

        st = new StringTokenizer(br.readLine());
        int[] arr = new int[n];
        for(int i = 0; i < n; i++){
            arr[i] = Integer.parseInt(st.nextToken());
        }


        // 입력받은 수 정렬해 제일 큰 수, 두 번째로 큰 수 저장
        Arrays.sort(arr);
        int first = arr[n-1];
        int second = arr[n-2];

        // 단순 반복
//        int result = 0;
//        int count = 0;
//        for (int i = 0; i < m; i++){
//            if (count < k){
//                result+= first;
//                count++;
//            } else {
//                result += second;
//                count = 0;
//            }
//        }
//        System.out.println(result);

        // 패턴 찾기
        int count = m / (k+1) * k; // 가장 큰 수 횟수
        count += m % (k+1); // 나누어떨어지지 않는 경우

        int result = 0;
        result += count * first;
        result += (m-count) * second;

        System.out.println(result);
    }

}
