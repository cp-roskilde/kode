#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define datatype char

datatype board[256];

int is_safe(int row) {
    datatype br = board[row];
    for (int i = 0; i < row; i++) {
        datatype bi = board[i];
        if (abs(bi - br) == row - i)
            return 0;
    }
    return 1;
}

long calc_solutions(int size) {
    long solutions = 0;

    long vertical = 0;

    int row = 0;
    board[0]=-1;
    while (row >= 0) {
        if (++board[row] >= size) {
            vertical &= ~(1<<board[--row]);
        } else if (((1<<board[row])&vertical)==0 && is_safe(row)) {
            if (row == size - 1) {
                solutions++;
                vertical &= ~(1<<board[--row]);
            } else {
                vertical |= 1<<board[row];
                board[++row] = -1;
            }
        }
    }

    return solutions;
}

long board2[32];

int is_safe2(int row) {
    long br = board2[row];
    for (int i = 0; i < row; i++) {
        long bi = board2[i];
        int shift = row - i;
        long bil = bi << shift;
        long bir = bi >> shift;
        if ((bir == br) || (bil == br))
            return 0;
    }
    return 1;
}

long calc_solutions2(int size) {
    long solutions = 0;

    long vertical = 0;
    long startRow = 1<<size;
    
    int row = 0;
    board2[0]=startRow;
    while (row >= 0) {
        board2[row] >>= 1;
        if (board2[row] == 0) {
            vertical &= ~(board2[--row]);
        } else if ((board2[row]&vertical)==0 && is_safe2(row)) {
            if (row == size - 1) {
                solutions++;
                vertical &= ~(board2[--row]);
            } else {
                vertical |= board2[row];
                board2[++row] = startRow;
            }
        }
    }

    return solutions;
}

int main() {
    
    for (int i = 1; i <= 15; i++) {
        clock_t start = clock();
        long solutions = calc_solutions2(i);
        clock_t end = clock();
        printf("Execution time: %f seconds for board size %i with %li solutions.\n", (double)(end - start) / CLOCKS_PER_SEC, i, solutions);
    }

    return 0;
}
