CC = gcc
CFLAGS = -Wall -Wextra -O2 -Iinclude
SRC_DIR = src
INC_DIR = include
TEST_DIR = tests
BUILD_DIR = build
BIN_DIR = bin

TARGET = $(BIN_DIR)/mergesort
TEST_TARGET = $(BIN_DIR)/test_mergesort

SRCS = $(SRC_DIR)/mergesort_k.c
OBJS = $(BUILD_DIR)/mergesort_k.o

all: $(TARGET)

$(TARGET): $(OBJS) $(BUILD_DIR)/main.o | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@

$(TEST_TARGET): $(OBJS) $(BUILD_DIR)/test_mergesort.o | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_mergesort.o: $(TEST_DIR)/test_mergesort.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

test: $(TEST_TARGET)
	@./$(TEST_TARGET)

benchmark: $(TARGET)
	@./$(TARGET) -b -n 100000

run: $(TARGET)
	@./$(TARGET) -r -n 30 -k 4

clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)

.PHONY: all test benchmark run clean

