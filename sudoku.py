# encoding: utf-8

import fileinput
from dlx import DLX
from optparse import OptionParser


class SudokuError(Exception):
    """
    Raised when any error related to Sudoku is found during construction
    and validation such as unexpected values or contradictions.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.encode('string_escape')


class Sudoku(object):
    """
    Complete all necessary steps to solve a Sudoku challenge using
    Dancing Links (DLX) including validating the challenge and building and
    validating the possible solution found by DLX.

    The expected input is one line of 81 characters where each unknown digit
    is represented as a '.' (dot).
    """

    def __init__(self, validate, pretty):
        self.validate = validate
        self.pretty = pretty
        self.grids = []
        self.solution = {}

    def solve(self, line):
        """
        Return list of solutions from specified line.
        Return empty list if no solutions are found and return at most
        one solution if validation is enabled or all solutions if validation
        is disabled. It is possible for a Sudoku challenge to have more than
        one solution but such challenge is concidered to be an invalid.
        """
        grid = self.build_challenge(line)

        dlx = DLX.from_sudoku(grid, self.result)
        dlx.run(self.validate)

        return self.grids

    def build_challenge(self, line):
        """
        Returns 9x9 numpy array from specified line.
        SudokuError is raised if unexpected value is found.
        """
        grid = []
        for c in line:
            if c != '.':
                if c < '1' or c > '9':
                    msg = 'Unexpected value "%s" when building challenge.' % c
                    raise SudokuError(msg)
                grid.append(int(c))
            else:
                grid.append(0)

        # return array(grid).reshape(9, 9)
        return [grid[i*9:(i+1)*9] for i in xrange(9)]

    def build_solution(self, s):
        """
        Return 9x9 grid from a solution found by DLX.
        """
        rows = []
        for k in s:
            rows.append(k.ID)
        rows.sort()

        grid = []
        for row in rows:
            grid.append(row % 9 + 1)

        # return array(grid).reshape(9, 9)
        return [grid[i * 9:(i + 1) * 9] for i in xrange(9)]

    def result(self, solutions, s):
        """
        Build, validate and save recieved solution.
        SudokuError is raised if validation is enabled and more than one
        solution exist or contradiction is found in solution.
        """
        grid = self.build_solution(s)

        if self.validate:
            if solutions > 1:
                msg = 'More than one solution exist.'
                raise SudokuError(msg)

        # transform to solution in dict
        self.format_solution(grid)

        if self.pretty:
            self.grids.append(self.format_pretty(grid))
        else:
            self.grids.append(self.format_simple(grid))

    def format_solution(self, grid):
        for r, a in enumerate(grid):
            for c, s in enumerate(a):
                self.solution[r, c] = s

    def format_simple(self, grid):
        """
        Return solution in the same format as expected input line.
        """
        f = ''
        for s in grid.ravel():
            f += str(s)
        return f

    def format_pretty(self, grid):
        """
        Return solution in a more human readable format.
        """
        f = '+-------+-------+-------+\n'
        for i, s in enumerate(grid):
            num = str(s)[1:-1].replace(',', '')
            f += '| %s | %s | %s |\n' % (num[0:5], num[6:11], num[12:17])
            if (i + 1) % 3 == 0:
                f += '+-------+-------+-------+'
                if (i + 1) < len(grid):
                    f += '\n'
        return f


def print_error(n, msg):
    print('sudoku: Error on line %s: %s' % (n, msg))


def print_solutions(grids):
    for grid in grids:
        print(grid)


def solve_line(sudoku, line, line_num):
    if len(line) < 82 or line[81] != '\n':
        print_error(line_num, 'Input line must be exactly 81 chars long.')
    else:
        # grids = []
        try:
            grids = sudoku.solve(line[:81])  # slice off '\n'
        except SudokuError as e:
            print_error(line_num, e)
        else:
            print_solutions(grids)


def solve_line_by_line(options, args):
    sudoku = Sudoku(options.validate, options.pretty)
    for line in fileinput.input(args):
        solve_line(sudoku, line, fileinput.lineno())


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option(
        '-v',
        '--validate',
        dest='validate',
        help='validate solution (longer search time)',
        action='store_true'
    )
    parser.add_option(
        '-p',
        '--pretty',
        dest='pretty',
        help='pretty print solution',
        action='store_true'
    )
    options, args = parser.parse_args()

    try:
        solve_line_by_line(options, args)
    except IOError as e:
        print('sudoku: %s' % e)
    except (KeyboardInterrupt, SystemExit) as e:
        print('')
        print('sudoku: Interrupt caught ... exiting')
