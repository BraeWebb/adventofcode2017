#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../api.h"

int sum_matching(char* line, int max, int (*func)(int, int)) {
    int sum = 0;
    for (int i = 0; i < max; i++) {
        if (line[i] == line[func(i, max) % max]) {
			sum += (int) (line[i] - '0');
		}
    }
    return sum;
}

int addOne(int i, int max) {
    return i + 1;
}

int halfway(int i, int max) {
    return i + (max / 2);
}

int main(int argc, char** argv) {
	Input* input = load_input();

	char* string = input->lines[0];
	int length = input->sizes[0];

    printf("%d\n", sum_matching(string, length, addOne));
    printf("%d\n", sum_matching(string, length, halfway));
}
