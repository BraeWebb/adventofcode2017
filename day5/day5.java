import java.util.ArrayList;
import java.util.Scanner;

public class day5 {
    private static int jump(Integer[] numbers, Replacer replacer) {
        int current = 0;
        int last = 0;
        int count = 0;
        while (current >= 0 && current < numbers.length) {
            last = current;
            current += numbers[current];
            numbers[last] = replacer.replace(numbers[last]);
            count += 1;
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        ArrayList<Integer> linesArray = new ArrayList<>();
        while (scan.hasNext()) {
            linesArray.add(scan.nextInt());
        }
        Integer[] partOne = linesArray.toArray(new Integer[]{});
        Integer[] partTwo = partOne.clone();

        Replacer addOne = (int oldValue) -> oldValue + 1;
        Replacer stranger = (int oldValue) -> oldValue < 3 ? oldValue + 1 : oldValue -1;

        System.out.println(jump(partOne, addOne));
        System.out.println(jump(partTwo, stranger));
    }
}

interface Replacer {
    int replace(int oldValue);
}