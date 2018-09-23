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

    sudoku = Sudoku(pretty=True)
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



