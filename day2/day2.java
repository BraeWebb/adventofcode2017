import java.io.BufferedInputStream;
import java.util.*;

public class day2 {
    private static int checkSum(String[] lines, Checksum checksumFunc) {
        int sum = 0;
        for (int i = 0; i < lines.length; i++) {
            String[] strings = lines[i].split("\t");
            int[] numbers = new int[strings.length];

            for (int j = 0; j < strings.length; j++) {
                numbers[j] = Integer.valueOf(strings[j]);
            }

            sum += checksumFunc.check(numbers);
        }
        return sum;
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(new BufferedInputStream(System.in));

        ArrayList<String> linesArray = new ArrayList<>();
        while (scan.hasNext()) {
            linesArray.add(scan.nextLine());
        }
        String[] lines = linesArray.toArray(new String[]{});

        Checksum minMinusMax = (int[] numbers) -> {
            int max = Arrays.stream(numbers).max().getAsInt();
            int min = Arrays.stream(numbers).min().getAsInt();

            return max - min;
        };

        Checksum evenNumbers = (int[] numbers) -> {
            for (int i = 0; i < numbers.length; i++) {
                for (int j = 0; j < numbers.length; j++) {
                    if ((numbers[i] % numbers[j] == 0) && (numbers[i] != numbers[j])) {
                        return numbers[i] / numbers[j];
                    }
                }
            }
            return 0;
        };

        System.out.println(checkSum(lines, minMinusMax));
        System.out.println(checkSum(lines, evenNumbers));
    }
}

interface Checksum {
    int check(int[] numbers);
}