package programmers.lv1;
import java.util.*;

public class PCCE10번_데이터분석 {

    class Solution {
        public int[][] solution(int[][] data, String ext, int val_ext, String sort_by) {

            // ext 컬럼 index 찾기
            int extIdx = getidx(ext);
            int sortIdx = getidx(sort_by);

            // ext 기준 정렬
            Arrays.sort(data, (a, b) -> a[extIdx] - b[extIdx]);

            // ext < val_ext 필터링
            List<int[]> filtered = new ArrayList<>();
            for(int[] row : data){
                if (row[extIdx] < val_ext){
                    filtered.add(row);
                }
            }

            // sort_by 기준 정렬
            filtered.sort((a, b) -> a[sortIdx] - b[sortIdx]);

            // 배열로 전환
            return filtered.toArray(new int[filtered.size()][]);

        }

        private int getidx(String ext){
            switch (ext) {
                case "code": return 0;
                case "date": return 1;
                case "maximum": return 2;
                case "remain": return 3;
            }
            return -1;
        }
    }
}
