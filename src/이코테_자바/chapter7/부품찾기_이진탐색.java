package 이코테_자바.chapter7;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class 부품찾기_이진탐색 {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] arr = new int[n];
        for(int i = 0; i < n; i++){
            arr[i] = Integer.parseInt(st.nextToken());
        }

        int m = Integer.parseInt(br.readLine());
        st = new StringTokenizer(br.readLine());
        int[] target = new int[m];
        for(int i = 0; i < m; i++){
            target[i] = Integer.parseInt(st.nextToken());
        }

        StringBuilder sb = new StringBuilder();
        for(int x : target){
            boolean result = binary_search(arr, x, 0, n-1);
            if (result){
                sb.append("yes").append(" ");
            } else{
                sb.append("no").append(" ");
            }
        }
        System.out.println(sb.toString());
    }


    static boolean binary_search(int[] arr, int target, int start, int end){
        while(start <= end){
            int mid = (start + end) / 2;
            if (arr[mid] == target) return true;
            else if (arr[mid] > target) end = mid-1;
            else start = mid + 1;
        }
        return false;
    }
}
