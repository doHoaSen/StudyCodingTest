package 이코테_자바.chapter8;

import java.math.BigInteger;

public class 피보나치_반복적8_4 {

    public static void main(String[] args) {
        BigInteger[] d = new BigInteger[100];
        d[1] = BigInteger.ONE;
        d[2] = BigInteger.ONE;

        int n = 99;

        for (int i = 3; i <= n; i++) {
            d[i] = d[i - 1].add(d[i - 2]);
        }

        System.out.println(d[n]);
    }
}
