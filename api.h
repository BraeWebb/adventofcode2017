#ifndef API_H
#define API_H

#define BUFFER_SIZE 256

typedef struct Input {
	char** lines;
	int* sizes;
	int count;
} Input;

typedef struct SplitResult {
	char** strings;
	int count;
} SplitResult;

Input* load_input();

SplitResult* split(char* string, char character);

#endif