package 프로그래머스.lv1;

public class 진법3_뒤집기 {
    public int solution(int n) {
        String num3 = Integer.toString(n, 3);   // 3진수 변환
        String reversed = new StringBuilder(num3).reverse().toString();
        return Integer.parseInt(reversed, 3);   // 3진수 → 10진수 변환
    }
}
