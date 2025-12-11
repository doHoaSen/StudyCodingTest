package Programmers.lv1;

public class 크기가_작은_부분문자열 {
    public int solution(String t, String p){
        int answer = 0;
        for(int i = 0; i < t.length() - p.length() + 1; i++){
            String str = t.substring(i, i+ p.length());
            if(Long.parseLong(str) <= Long.parseLong(p)) answer++;
        }
        return answer;
    }
}
