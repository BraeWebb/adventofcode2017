#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../api.h"

int main(int argc, char** argv) {
	Input* input = load_input();

	for (int i = 0; i < input->count; i++) {
		printf("%s\n", input->lines[i]);
	}

	return 0;
}