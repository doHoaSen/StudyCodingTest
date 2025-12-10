package 이코테_자바.chapter6;

public class 선택정렬6_1 {
    public static void main(String[] args){
        int[] array = {7, 5, 9, 0, 3, 1, 6, 2, 4, 8};

        for(int i = 0; i < array.length; i++){
            int minIdx = i;
            for(int j = i + 1; j < array.length; j++){
                if(array[minIdx] > array[j]){
                    minIdx = j;
                }
            }
            int temp = array[minIdx];
            array[minIdx] = array[i];
            array[i] = temp;
        }
        for(int i : array){
            System.out.print(i);
        }
    }
}
