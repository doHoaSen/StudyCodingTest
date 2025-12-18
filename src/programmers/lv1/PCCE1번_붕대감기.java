package programmers.lv1;

public class PCCE1번_붕대감기 {
    class Solution {
        public int solution(int[] bandage, int health, int[][] attacks) {
            int t = bandage[0];
            int heal = bandage[1];
            int bonus = bandage[2];

            int curHealth = health;
            int combo = 0;

            int idx = 0;  // attacks 포인터
            int lastTime = attacks[attacks.length - 1][0];

            for (int time = 0; time <= lastTime; time++) {

                // 공격 시간
                if (idx < attacks.length && attacks[idx][0] == time) {
                    int damage = attacks[idx][1];

                    curHealth -= damage;
                    if (curHealth <= 0) return -1;

                    combo = 0;
                    idx++;

                } else {
                    // 회복 시간
                    combo++;
                    curHealth += heal;

                    if (combo == t) {
                        curHealth += bonus;
                        combo = 0;
                    }

                    // 최대 체력 초과 금지
                    if (curHealth > health) curHealth = health;
                }
            }

            return curHealth;
        }
    }

}
