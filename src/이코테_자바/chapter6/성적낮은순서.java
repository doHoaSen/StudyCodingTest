package 이코테_자바.chapter6;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class 성적낮은순서 {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int N = Integer.parseInt(br.readLine());
        List<Student> list = new ArrayList();
        for(int i = 0; i < N; i++){

            StringTokenizer st = new StringTokenizer(br.readLine());
            String name = st.nextToken();
            int score = Integer.parseInt(st.nextToken());

            list.add(new Student(name, score));
        }

        list.sort(Comparator.comparingInt(s -> s.score));

        for(Student s: list){
            System.out.print(s.name + " ");
        }
    }
}

class Student{
    String name;
    int score;

    public Student(String name, int score){
        this.name = name;
        this.score = score;
    }
}
