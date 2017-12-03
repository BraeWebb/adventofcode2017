#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "api.h"

Input* load_input() {
	Input* input = malloc(sizeof(Input));

	int count = 1;
	char** strings = malloc(sizeof(char*) * count);
	int* sizes = malloc(sizeof(int) * count);


	char str[BUFFER_SIZE];
    char* string = malloc(sizeof(char) * BUFFER_SIZE);
    int length = 0;
    while (fgets(str, sizeof(str), stdin) != NULL) {
        string = realloc(string, sizeof(char) * length + BUFFER_SIZE);
    	memcpy(string + length, str, strlen(str) + 1);
		length += strlen(str);

		if (string[strlen(string) - 1] == '\n') {

			string[length-1] = '\0';

			strings[count-1] = string;
			sizes[count-1] = length-1;

			count++;

			strings = realloc(strings, sizeof(char*) * count);
			sizes = realloc(sizes, sizeof(int) * count);

			string = malloc(sizeof(char) * BUFFER_SIZE);
			length = 0;
		}
    }

    strings[count-1] = string;
	sizes[count-1] = length;

	input->lines = strings;
	input->sizes = sizes;
	input->count = count;

    return input;
}