#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include "../api.h"

bool is_anagram(char* first, char* second) {
	int firstLetters[26] = {0};
	int secondLetters[26] = {0};

	for (int i = 0; i < strlen(first); i++) {
		firstLetters[first[i] - 'a']++;
	}

	for (int i = 0; i < strlen(second); i++) {
		secondLetters[second[i] - 'a']++;
	}

	for (int i = 0; i < 26; i++) {
		if (firstLetters[i] != secondLetters[i]) {
			return false;
		}
	}
	return true;
}

bool is_valid(char* phrase, bool (*condition)(char*, char**, int)) {
	SplitResult* splits = split(phrase, ' ');

	char** words = malloc(sizeof(char*) * splits->count);

	for (int i = 0; i < splits->count; i++) {
		if (!condition(splits->strings[i], words, i)) {
			return false;
		}
		words[i] = splits->strings[i];
	}

	return true;
}

bool is_in(char* word, char** words, int wordCount) {
	for (int i = 0; i < wordCount; i++) {
		if (strcmp(word, words[i]) == 0) {
			return false;
		}
	}
	return true;
}

bool has_anagram(char* word, char** words, int wordCount) {
	for (int i = 0; i < wordCount; i++) {
		if (is_anagram(word, words[i])) {
			return false;
		}
	}
	return true;
}

int main(int argc, char** argv) {
	Input* input = load_input();

	int part1 = 0;
	int part2 = 0;

	for (int i = 0; i < input->count; i++) {
		if (is_valid(input->lines[i], is_in)) {
			part1++;
		}
		if (is_valid(input->lines[i], has_anagram)) {
			part2++;
		}
	}

	printf("%d\n", part1);
	printf("%d\n", part2);

	return 0;
}