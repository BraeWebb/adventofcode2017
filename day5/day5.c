#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../api.h"

int jump(int* numbers, int numberCount, int (*replace)(int)) {
    int current, last, count = 0;
    while (current >= 0 && current < numberCount) {
        last = current;
        current += numbers[current];
        numbers[last] = replace(numbers[last]);
        count += 1;
    }
    return count;
}

int add_one(int oldValue) {
	return oldValue + 1;
}

int stranger(int oldValue) {
	if (oldValue >= 3) {
		return oldValue - 1;
	}
	return oldValue + 1;
}

int main(int argc, char** argv) {
	Input* input = load_input();

	int* partOne = malloc(sizeof(int) * input->count);
	for (int i = 0; i < input->count; i++) {
		partOne[i] = atoi(input->lines[i]);
	}

	printf("%d\n", jump(partOne, input->count, add_one));

	int* partTwo = malloc(sizeof(int) * input->count);
	for (int i = 0; i < input->count; i++) {
		partTwo[i] = atoi(input->lines[i]);
	}

	printf("%d\n", jump(partTwo, input->count, stranger));
}