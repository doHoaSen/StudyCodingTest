package 이코테_자바.chapter6;

public class 계수정렬6_6 {
    public static void main(String args[]){
        int[] array = {7, 5, 9, 0, 3, 1, 6, 2, 9, 1, 4, 8, 0, 5, 2};

        int[] count = new int[10];

        for(int i = 0; i < array.length; i++){
            count[array[i]]++;
        }

        for(int i = 0; i < count.length; i++){
            for(int j = 0; j < count[i]; j++){
                System.out.print(i + " ");
            }
        }

        // 시간복잡도 O(N+K)
        // - 데이터 개수 N, 데이터 중 최대값의 크기 K
        // 데이터의 크기가 한정되어 있고 데이터의 크기가 많이 중복되어 있을수록 유리
    }
}
