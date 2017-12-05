import java.util.Scanner;

public class day1 {

    private static int sumMatching(String line, FindMatch matcher) {
        int max = line.length();
        int sum = 0;

        for (int i = 0; i < line.length(); i++) {
            if (line.charAt(i) == line.charAt(matcher.find(i, max) % max)) {
                sum += Character.getNumericValue(line.charAt(i));
            }
        }

        return sum;
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        String line = scan.nextLine();

        System.out.println(sumMatching(line, (int i, int max) -> i + 1));
        System.out.println(sumMatching(line, (int i, int max) -> i + (max / 2)));
    }
}

interface FindMatch {
    int find(int i, int max);
}