package programmers.lv2;

public class 피보나치수 {

    /* =========================
       1️⃣ Bottom-Up 버전
       ========================= */
    static class Solution {
        public int solution(int n) {
            int[] dp = new int[n + 1];

            dp[0] = 0;
            dp[1] = 1;

            for (int i = 2; i <= n; i++) {
                dp[i] = (dp[i - 2] + dp[i - 1]) % 1234567;
            }

            return dp[n];
        }
    }

    /* =========================
       2️⃣ Top-Down 버전
       ========================= */
    static class Solution2 {

        static int[] memo;
        static final int MOD = 1234567;

        public int solution(int n) {
            memo = new int[n + 1];
            return fibo(n);
        }

        private int fibo(int n) {
            if (n == 0) return 0;
            if (n == 1) return 1;

            if (memo[n] != 0) {
                return memo[n];
            }

            memo[n] = (fibo(n - 1) + fibo(n - 2)) % MOD;
            return memo[n];
        }
    }
}