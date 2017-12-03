CC=gcc
FLAGS=-Wall -pedantic --std=gnu99
DAYS := $(wildcard */.)

all: $(DAYS)
	@for dir in $(DAYS); do \
		day=$${dir:0:-2}; \
		make build DAY=$$day; \
	done

api.o: api.c api.h
	$(CC) $(FLAGS) -c api.c -o api.o

build: clean $(DAY)/$(DAY).c api.o
	$(CC) $(FLAGS) $(DAY)/$(DAY).c api.o -o $(DAY)/$(DAY)

clean: $(DAYS)
	@for dir in $(DAYS); do \
		day=$${dir:0:-2}; \
		rm -f $$day/$$day.exe; \
	done