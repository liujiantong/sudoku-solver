#!/usr/bin/env python
# encoding: utf-8


def solve(input_dict):
    import time
    import random
    # TODO: implement algorithm here
    print 'input_dict: %s' % input_dict
    time.sleep(3)

    # fake solution
    solution = {}
    for blckId in xrange(9):
        for row in xrange(3):
            for col in xrange(3):
                solution[(blckId, row, col)] = random.randrange(1, 10)
    return solution
