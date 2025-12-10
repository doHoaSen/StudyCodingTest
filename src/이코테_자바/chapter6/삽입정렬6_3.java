package 이코테_자바.chapter6;

public class 삽입정렬6_3 {
    public static void main(String args[]){
        int[] array = {7, 5, 9, 0, 3, 1, 6, 2, 4, 8};

        for(int i = 0; i < array.length; i++){
            for (int j = i; j > 0; j--){
                // 한 칸씩 왼쪽으로 이동하며, 자기보다 작은 데이터를 만나면 그 자리에서 멈춤
                if(array[j] < array[j-1]){
                    int temp = array[j];
                    array[j] = array[j-1];
                    array[j-1] = temp;
                } else break;
            }
        }
        for(int i : array){
            System.out.print(i);
        }
    }
    // 현재 리스트의 데이터가 거의 정렬되어 있는 상태라면 매우 빠르게 동작함
    // 최선의 경우 O(N)의 시간복잡도
}
