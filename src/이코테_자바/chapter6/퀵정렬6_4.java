package 이코테_자바.chapter6;

public class 퀵정렬6_4 {
    public static void main(String args[]){
        int[] array = {7, 5, 9, 0, 3, 1, 6, 2, 4, 8};

        quick_sort(array, 0, array.length-1);
        for(int i : array){
            System.out.print(i);
        }
    }

    static void quick_sort(int[] arr, int start, int end) {
        if (start >= end) return;

        int pivot = start;
        int left = start + 1;
        int right = end;

        while (left <= right) {

            // 피벗보다 큰 데이터 찾기 (왼쪽에서 오른쪽으로)
            while (left <= end && arr[left] <= arr[pivot]) left++;

            // 피벗보다 작은 데이터 찾기 (오른쪽에서 왼쪽으로)
            while (right > start && arr[right] >= arr[pivot]) right--;

            if (left > right) {
                // 엇갈렸다면 small(right)와 pivot 교환
                int temp = arr[right];
                arr[right] = arr[pivot];
                arr[pivot] = temp;
            } else {
                // 엇갈리지 않았다면 small(left)과 big(right) 교환
                int temp = arr[left];
                arr[left] = arr[right];
                arr[right] = temp;
            }
        }

        // 분할 이후 두 부분 배열 정렬
        quick_sort(arr, start, right - 1);
        quick_sort(arr, right + 1, end);
    }

    // 평균 시간 복잡도 O(NlogN)
}
