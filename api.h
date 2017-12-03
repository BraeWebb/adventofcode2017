#ifndef API_H
#define API_H

#define BUFFER_SIZE 16

typedef struct Input {
	char** lines;
	int* sizes;
	int count;
} Input;

Input* load_input();

#endif