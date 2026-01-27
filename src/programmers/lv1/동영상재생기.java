package programmers.lv1;

public class 동영상재생기 {
    class Solution {
        public String solution(String video_len, String pos, String op_start, String op_end, String[] commands) {
            int videoLen = convertToSeconds(video_len);
            int position = convertToSeconds(pos);
            int opStart = convertToSeconds(op_start);
            int opEnd = convertToSeconds(op_end);

            position = skipOpening(position, opStart, opEnd);
            for (String command: commands) {
                if (command.equals("prev")) {
                    position = Math.max(position - 10, 0);
                } else {
                    position = Math.min(position + 10, videoLen);
                }
                position = skipOpening(position, opStart, opEnd);
            }

            String answer = convertToString(position);
            return answer;
        }

        public int skipOpening(int t, int op_start, int op_end){
            if (t >= op_start && t <= op_end){
                return op_end;
            }
            return t;
        }

        // 문자열 -> 초
        public int convertToSeconds(String s){
            String[] arr = s.split(":");
            int mm = Integer.parseInt(arr[0]);
            int ss = Integer.parseInt(arr[1]);
            return mm * 60 + ss;
        }

        // 초 -> 문자열
        String convertToString(int t){
            int mm = t / 60;
            int ss = t % 60;
            return String.format("%02d:%02d", mm, ss);
        }
    }
}
