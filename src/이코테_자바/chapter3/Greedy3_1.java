package 이코테_자바.chapter3;

class Greedy3_1 {
    public static void main(String args[]){
        int n = 1260;
        int count = 0;

        int[] coin_type = {500, 100, 50, 10};

        for (int coin : coin_type){
            count += n / coin;
            n %= coin;
        }

        System.out.println(count);
    }
}