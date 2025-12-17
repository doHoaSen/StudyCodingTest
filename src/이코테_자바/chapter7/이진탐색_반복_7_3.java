package 이코테_자바.chapter7;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class 이진탐색_반복_7_3 {
    public static void main(String[] args) throws IOException {
        BufferedReader br= new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int target = Integer.parseInt(st.nextToken());

        int[] arr = new int[n];
        st = new StringTokenizer(br.readLine());
        for(int i = 0; i < n; i++){
            arr[i] = Integer.parseInt(st.nextToken());
        }

        int result = binary_search(arr, target, 0, n-1);
        if (result == -1){
            System.out.println("원소가 존재하지 않습니다.");
        } else {
            System.out.println(result + 1);
        }
    }

    private static int binary_search(int[] arr, int target, int start, int end){
        while(start <= end){
            int mid = (start + end) / 2;
            if(arr[mid] == target) return mid;
            else if (arr[mid] > target) end = mid - 1;
            else start = mid + 1;
        }
        return -1;
    }
}
// 시간복잡도 O(logN)
// 처리해야 할 데이터 개수나 값이 1000만 단위 이상 넘어가면 이진탐색과 같이
// O(logN) 속도 내야 하는 알고리즘 떠올려야 하는 문제가 많다!
