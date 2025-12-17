package programmers.lv1;

public class 공원산책 {
    class Solution {
        public int[] solution(String[] park, String[] routes) {
            int h = park.length;
            int w = park[0].length();
            int x = 0, y = 0;

            // S 찾아 시작 위치 세팅
            for(int i = 0; i < h; i++){
                for(int j = 0; j < w; j++){
                    if(park[i].charAt(j) == 'S'){
                        x = i;
                        y = j;
                    }
                }
            }

            // 방향
            int[] dx = {-1, 1, 0, 0}; // N S W E
            int[] dy = {0, 0, -1, 1};
            String d = "NSWE";



            for(String route: routes){
                String[] r = route.split(" ");
                String dir = r[0];
                int dist = Integer.parseInt(r[1]);

                int idx = d.indexOf(dir);
                int nx= x;
                int ny = y;
                boolean ok = true;

                // 한 칸씩 이동하며 체크
                for(int k = 0; k < dist; k++){
                    nx += dx[idx];
                    ny += dy[idx];
                    if (nx < 0|| ny < 0 || nx >= h || ny >= w){
                        ok = false;
                        break;
                    }

                    if(park[nx].charAt(ny) == 'X'){
                        ok = false;
                        break;
                    }

                }
                if(ok){
                    x = nx;
                    y = ny;
                }

            }
            return new int[] {x, y};
        }
    }
}
