#!/usr/bin/env python
# encoding: utf-8


def solve(matrix_input):
    """
    Solve sudoku
    :param matrix_input: (row, col) -> value
    :return: matrix solution: (row, col) -> value
    """
    print 'number_input: %s' % matrix_input

    # TODO: fake solution algorithm start
    import time
    import random
    time.sleep(2)

    solution = {}
    for row in xrange(9):
        for col in xrange(9):
            solution[(row, col)] = random.randrange(1, 10)

    for k, v in matrix_input.iteritems():
        row, col = k
        solution[(row, col)] = v
    # TODO: fake solution algorithm end

    return solution

