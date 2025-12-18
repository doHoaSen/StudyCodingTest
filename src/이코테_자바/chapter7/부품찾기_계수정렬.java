package 이코테_자바.chapter7;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class 부품찾기_계수정렬 {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] arr = new int[10000001];
        for(int i = 0; i < n; i++){
            int temp = Integer.parseInt(st.nextToken());
            arr[temp] = 1;
        }

        int m = Integer.parseInt(br.readLine());
        st = new StringTokenizer(br.readLine());
        int[] target = new int[m];
        for(int i = 0; i < m; i++){
            target[i] = Integer.parseInt(st.nextToken());
        }

        StringBuilder sb = new StringBuilder();
        for(int t:target){
            if (arr[t] == 1){
                sb.append("yes").append(" ");
            } else {
                sb.append("no").append(" ");
            }
        }

        System.out.println(sb.toString());
    }
}
