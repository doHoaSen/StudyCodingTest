package 이코테_자바.chapter6;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class 위에서아래로 {
    public static void main(String[] args) throws IOException {
        // 입력
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int N = Integer.parseInt(br.readLine());
        int[] arr = new int[N];
        for(int i = 0; i < N; i++){
            arr[i] = Integer.parseInt(br.readLine());
        }

        // 오름차순 정렬
        Arrays.sort(arr);

        // 결과 공백으로 구분해 뒤집어 출력
        for(int i = N-1; i >= 0; i--){
            System.out.print(arr[i] + " ");
        }
    }

    // 정렬 방식을 함수로 구현한다면
    public Integer[] sort(Integer[] arr) {
        Arrays.sort(arr, new Comparator<Integer>() {
            @Override
            public int compare(Integer o1, Integer o2) {
                if (o1 < o2) return 1;
                else if (o1 > o2) return -1;
                else return 0;
                // o1 < o2 → o2가 앞 → 양수 반환
                // o1 > o2 → o1이 앞 → 음수 반환
            }
        });
        return arr;
    }

    public void sort2(Integer[] arr){
        Arrays.sort(arr, (o1, o2) -> {
            if (o1 < o2) return 1;
            else if (o1 > o2) return -1;
            else return 0;
        });
    }
}
