"""
n x n queen problem

goal: given a chess board of N x N size - find as many possible placements of queens
"""


def build_board(n):
    return [[False for _ in range(n)] for _ in range(n)]

b = build_board(5)


def is_valid(b):
    board_size = len(b[0])

    for row in xrange(board_size):
        for col in xrange(board_size):
            if b[row][col]:
                invalid = any([b[x][col] for x in xrange(0, row-1, 1)]) or \
                    any([b[x][col] for x in xrange(x+1, board_size, 1)])  # horizontal
                if invalid:
                    return False

                invalid = any([b[row][y] for y in xrange(0, col - 1, 1)]) or \
                    any([b[row][y] for y in xrange(col, board_size, 1)])  # veritcal
                if invalid:
                    return False

b[0][0] = True
b[4][0] = True

print is_valid(b)





