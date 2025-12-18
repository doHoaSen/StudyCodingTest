package 이코테_자바.chapter7;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class 떡볶이떡만들기 {
    static int[] arr;
    static int m;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        m = Integer.parseInt(st.nextToken());

        arr = new int[n];
        st = new StringTokenizer(br.readLine());
        for(int i = 0 ; i < n; i++){
            arr[i] = Integer.parseInt(st.nextToken());
        }
        Arrays.sort(arr);
        int result = search(arr, 0, arr[arr.length-1]);
        System.out.println(result);
    }

    static int search(int[]arr, int start, int end){
        int height = 0;
        while(start<=end){
            int total = 0;
            int mid = (start + end) / 2;
            for(int x : arr){
                if (x > mid){
                    total += x - mid;
                }
            }

            if (total < m){
                end = mid - 1;
            } else {
                height = mid;
                start = mid + 1;
            }
        }

        return height;
    }
}
