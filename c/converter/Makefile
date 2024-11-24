CC = gcc
CFLAGS = -Wall -Wextra -O2 -I. 
LDFLAGS = -lSDL2 -lm

SRCS = main.c 
OBJS = $(SRCS:.c=.o)
TARGET = converter

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)