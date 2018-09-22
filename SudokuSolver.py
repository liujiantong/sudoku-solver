#!/usr/bin/env python
# encoding: utf-8

from sudoku import Sudoku


def solve(matrix_input):
    """
    Solve sudoku
    :param matrix_input: (row, col) -> value
    :return: matrix solution: (row, col) -> value
    """

    line_input = _tx_input(matrix_input)
    print 'number_input: %s' % matrix_input
    print 'tx_input: %s' % line_input

    sudoku = Sudoku(False, True)
    grids = sudoku.solve(line_input)
    _print_grids(grids)

    return sudoku.solution


def _tx_input(matrix_input):
    cache = []
    for i in xrange(9):
        for j in xrange(9):
            cache.append(matrix_input.get((i, j), '.'))
    return ''.join(cache)


def _print_grids(grids):
    for grid in grids:
        print grid


def _mock(matrix_input):
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

