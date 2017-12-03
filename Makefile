CC=gcc
FLAGS=-Wall -pedantic --std=gnu99
DAYS := $(wildcard */.)

all: $(DAYS)
	@for dir in $(DAYS); do \
		day=$${dir:0:-2}; \
		make build DAY=$$day; \
	done

build: clean $(DAY)/$(DAY).c
	$(CC) $(FLAGS) $(DAY)/$(DAY).c -o $(DAY)/$(DAY)

clean: $(DAYS)
	@for dir in $(DAYS); do \
		day=$${dir:0:-2}; \
		rm -f $$day/$$day.exe; \
	done