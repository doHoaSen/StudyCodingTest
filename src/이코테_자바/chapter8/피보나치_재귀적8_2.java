package 이코테_자바.chapter8;

import java.math.BigInteger;

public class 피보나치_재귀적8_2 {
    static BigInteger[] d = new BigInteger[100];

    public static void main(String[] args) {
        System.out.println(fibo(99));
    }

    static BigInteger fibo(int x){
        if (x == 1 || x == 2){
            return BigInteger.ONE;
        }

        if (d[x] != null) return d[x];

        d[x] = fibo(x - 1).add(fibo(x - 2));
        return d[x];
    }
}
