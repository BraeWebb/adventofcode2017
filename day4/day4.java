import java.io.BufferedInputStream;
import java.util.*;

public class day4 {
    private static boolean isValid(String phrase, Validator validator) {
        String[] strings = phrase.split(" ");
        String[] words = new String[strings.length];
        int count = 0;
        for (int i = 0; i < strings.length; i++) {
            if (!validator.validate(strings[i], words)) {
                return false;
            }
            words[count++] = strings[i];
        }
        return true;
    }

    private static boolean isAnagram(String first, String second) {
        char[] firsts = first.toCharArray();
        if (second == null) {
            return false;
        }
        char[] seconds = second.toCharArray();
        Arrays.sort(firsts);
        Arrays.sort(seconds);
        return Arrays.equals(firsts, seconds);
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(new BufferedInputStream(System.in));

        Validator isIn = (String word, String[] words) -> {
            for (int i = 0; i < words.length; i++) {
                if (word.equals(words[i])) {
                    return false;
                }
            }
            return true;
        };

        Validator isAnagram = (String word, String[] words) -> {
            for (int i = 0; i < words.length; i++) {
                if (isAnagram(word, words[i])) {
                    return false;
                }
            }
            return true;
        };

        int validOne = 0;
        int validTwo = 0;
        while (scan.hasNext()) {
            String line = scan.nextLine();
            if (isValid(line, isIn)) {
                validOne += 1;
            }
            if (isValid(line, isAnagram)) {
                validTwo += 1;
            }
        }

        System.out.println(validOne);
        System.out.println(validTwo);
    }
}

interface Validator {
    boolean validate(String word, String[] words);
}