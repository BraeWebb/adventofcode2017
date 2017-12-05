#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>

#include "../api.h"

int checksum(char** lines, int lineCount, int (*checksum_func)(int*, int)) {
    int checksum = 0;
    for (int i = 0; i < lineCount; i++) {
		SplitResult* result = split(lines[i], '\t');

		int* numbers = malloc(sizeof(int) * result->count);

		for (int j = 0; j < result->count; j++) {
			sscanf(result->strings[j], "%d", &(numbers[j]));
		}

		checksum += checksum_func(numbers, result->count);
    }
    return checksum;
}

int max_minus_min(int* numbers, int numberCount) {
	int max = 0;
	int min = INT_MAX;

	for (int i = 0; i < numberCount; i++) {
		if (numbers[i] > max) {
			max = numbers[i];
		}
		if (numbers[i] < min) {
			min = numbers[i];
		}
	}

	return max - min;
}

int even_numbers(int* numbers, int numberCount) {
	for (int i = 0; i < numberCount; i++) {
		for (int j = 0; j < numberCount; j++) {
			if ((numbers[i] % numbers[j] == 0) && (numbers[i] != numbers[j])) {
				return numbers[i] / numbers[j];
			}
		}
	}
	return 0;
}

int main(int argc, char** argv) {
	Input* input = load_input();

    printf("%d\n", checksum(input->lines, input->count, max_minus_min));
    printf("%d\n", checksum(input->lines, input->count, even_numbers));
}