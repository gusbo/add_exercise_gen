#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
__author__ = 'gusbos'

from random import choice
from itertools import islice, ifilter, permutations, combinations_with_replacement, combinations, chain
from string import Template
import cProfile

candidate_numbers = range(40)

def horisontal_one(x1, x2, x3):
    return (x1 - x2) == x3


def horisontal_two(x4, x5, x6):
    return (x4 + x5) == x6


def horisontal_three(x7, x8, x9):
    return (x7 + x8) == x9


def construct_row_gen(row_predicate):
    return (t for t in combinations_with_replacement(candidate_numbers, 3) if row_predicate(*t))


def valid_first_row_gen():
    return construct_row_gen(horisontal_one)


def valid_second_row_gen():
    return construct_row_gen(horisontal_two)


def valid_third_row_gen():
    return construct_row_gen(horisontal_three)


def row_combinations_gen():
    return combinations_with_replacement(chain(valid_first_row_gen(), valid_second_row_gen(), valid_third_row_gen()), 3)


def row_permutations_gen():
    for combination in row_combinations_gen():
        for perm in permutations(combination):
            yield perm


def vertical_one(x1, x2, x3, x4, x5, x6, x7, x8, x9):
    return (x1 - x4) == x7


def vertical_two(x1, x2, x3, x4, x5, x6, x7, x8, x9):
    return (x2 - x5) == x8


def vertical_three(x1, x2, x3, x4, x5, x6, x7, x8, x9):
    return (x3 - x6) == x9


def gen_all_candidate_numbers():
    #Get all combinations of numbers satisfying first row constraint
    for combination in combinations(candidate_numbers, 9):
        print combination
        for permutation in permutations(combination):
            #print permutation
            yield permutation


def take_candidate_series(numbergenerator):
    #take 9 numbers
    while True:
        random_list = list(islice(numbergenerator, 9))
        #yield random_list
        for combination_of_random_list in permutations(random_list):
            yield combination_of_random_list


def run_constraints(candidate_series):
    """
    Constraints for the square:
    x1 + x2 = x3
    -    -    -
    x4 + x5 = x6
    =    =    =
    x7 + x8 = x9
    """
    (x1, x2, x3, x4, x5, x6, x7, x8, x9) = candidate_series

    def horisontal_one(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x1 + x2) == x3

    def horisontal_two(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x4 + x5) == x6

    def horisontal_three(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x7 + x8) == x9

    def vertical_one(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x1 - x4) == x7

    def vertical_two(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x2 - x5) == x8

    def vertical_three(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x3 - x6) == x9

    constraint_funcs = (horisontal_one, horisontal_two, horisontal_three, vertical_one, vertical_two, vertical_three)
    #Run all constraints
    for func in constraint_funcs:
        if not func(x1, x2, x3, x4, x5, x6, x7, x8, x9):
            return False
        #If all constraints pass return True
    return True





def run_vertical_constraints(candidate_series):
    def flatten_row_and_unpack(candidate_series):
        return chain(*candidate_series)

    (x1, x2, x3, x4, x5, x6, x7, x8, x9) = flatten_row_and_unpack(candidate_series)

    def vertical_one(x1, xx2, x3, x4, x5, x6, x7, x8, x9):
        return (x1 - x4) == x7

    def vertical_two(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x2 - x5) == x8

    def vertical_three(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x3 - x6) == x9

    constraint_funcs = (vertical_one, vertical_two, vertical_three)
    #Run all constraints
    for func in constraint_funcs:
        if not func(x1, x2, x3, x4, x5, x6, x7, x8, x9):
            return False
        #If all constraints pass return True
    return True

def run_vertical_constraints_only_plus(candidate_series):
    #flatten row and unpack
    (x1, x2, x3, x4, x5, x6, x7, x8, x9) = chain(*candidate_series)

    def vertical_one(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x1 + x4) == x7

    def vertical_two(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x2 + x5) == x8

    def vertical_three(x1, x2, x3, x4, x5, x6, x7, x8, x9):
        return (x3 + x6) == x9

    constraint_funcs = (vertical_one, vertical_two, vertical_three)
    #Run all constraints
    for func in constraint_funcs:
        if not func(x1, x2, x3, x4, x5, x6, x7, x8, x9):
            return False
        #If all constraints pass return True
    return True


def filter_fulfills_constraints(candidate_series_gen):
    return ifilter(run_constraints, candidate_series_gen)

square_template_str = """
    $x1 + $x2 = $x3
    -   -   -
    $x4 + $x5 = $x6
    =   =   =
    $x7 + $x8 = $x9
    """

square_template_str_plus_only = """
      + $x2 = $x3
    +   +   +
    $x4 +   = $x6
    =   =   =
    $x7 + $x8 = $x9
    """

def format_square(matched_series, square_template_str = square_template_str):
    (x1, x2, x3, x4, x5, x6, x7, x8, x9) = matched_series

    template = Template(square_template_str)
    return template.substitute(locals())




def find_solutions_old():
    for matched_series in filter_fulfills_constraints(gen_all_candidate_numbers()):
        print format_square(matched_series)
        
def find_solutions():
    solutions = ifilter(run_vertical_constraints_only_plus, row_permutations_gen())
    def is_not_zero_solution(row):
        return sum(chain(*row)) <> 0
    no_zero_solutions = ifilter(is_not_zero_solution,solutions)
    return no_zero_solutions

def print_solutions(solutions):
    for solution in solutions:
        print format_square(chain(*solution))

def random_solutions(solutions):
    #Yield randomly
    for solution in solutions:
        if choice((True,False)):
            yield solution

#print list(valid_first_row_gen())
#print run_constraints((9, 8, 17, 2, 3, 5, 7, 5, 12))
solutions = find_solutions()
outfilepath = "solutions.txt"

fp = open(outfilepath,"w")
print "writing solutions to file: %s" % outfilepath
solution_generator = (format_square(chain(*solution),square_template_str_plus_only) for solution in random_solutions(solutions))
with fp:
    fp.writelines(solution_generator)
#find_solutions()