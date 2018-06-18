#!/usr/bin/env python
# encoding: utf-8


def solve(input_dict):
    """
    Solve sudoku
    :param input_dict - sudoku input matrix whose key is matrix position
    :return:
    """
    print 'number_input: %s' % input_dict

    # TODO: fake solution algorithm start
    import time
    import random
    time.sleep(2)

    solution = {}
    for row in xrange(9):
        for col in xrange(9):
            solution[(row, col)] = random.randrange(1, 10)

    for k, v in input_dict.iteritems():
        row, col = k
        solution[(row, col)] = v
    # TODO: fake solution algorithm end
    
    return solution

