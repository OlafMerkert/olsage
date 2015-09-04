# -*- coding: utf-8; sage: t -*-

# various essential utility functions for working with sage


# imports
from sage.all import *
from sage.rings.polynomial.polynomial_element import is_Polynomial
from sage.rings.laurent_series_ring_element import is_LaurentSeries

import re

# wildcards
w = map(SR.wild, xrange(20))


# general utilities
def transpose(list_of_lists):
    return map(list, zip(*list_of_lists))

def chunks(l, n=2):
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]


# helper function writing simple tests
def test_it(*args):
    """Testing helper function. With an even number of arguments, with a
    string and a boolean in turn, collect all the strings for which
    the following boolean is false.
    """
    problems = [description
                for (description, test) in chunks(args, 2)
                if not test]
    if len(problems) == 0:
        return True
    else:
        return False, problems


# pretty printing
def lrepr(lst, repr=True, ret=False):
    if repr == "table":
        return trepr(lst)
    elif repr:
        for i, l in enumerate(lst):
            print "{0}: {1}".format(i, l.repr())
    else:
        for i, l in enumerate(lst):
            print "{0}: {1}".format(i, l)
    if ret:
        return lst

def trepr(lst, repr=True):
    if repr:
        return [[i, l.repr()] for i, l in enumerate(lst)]
    else:
        return [[i, l] for i, l in enumerate(lst)]
    if ret:
        return lst


# producing latex output

produce_latex = True


def latex_strip(string):
    """remove left and right parenthesis groupings, and also the {} around them."""
    string = re.sub("{?\\\\left", "", string)
    string = re.sub("\\\\right\\)}?", ")", string)
    string = re.sub("\\\\mathit{la}", "\\lambda", string)
    return string


def l(*args):
    if produce_latex:
        for a in args:
            print "\\begin{dmath*}[frame,breakdepth={4}]", latex_strip(latex(a)), "\\end{dmath*}"
    else:
        if len(args) == 1:
            return args[0]
        else:
            return args


# lazy sequences

class ComputableDoubleLinkedList(object):
    """A base class for infinite sequences that get computed on the fly."""
    def __init__(self, prev=None, next=None):
        self._prev = prev
        self._next = next

    def prev(self):
        if self._prev is None:
            raise IndexError
        elif self._prev is Ellipsis:
            self._prev = self.compute_prev()
        return self._prev

    def next(self):
        if self._next is None:
            raise IndexError
        elif self._next is Ellipsis:
            self._next = self.compute_next()
        return self._next

    def set_next(self, next):
        self._next = next

    def set_prev(self, prev):
        self._prev = prev

    def has_next(self):
        return (self._next is not None)

    def has_prev(self):
        return (self._prev is not None)

    def compute_next(self):
        return None

    def compute_prev(self):
        return None

    def __getitem__(self, i):
        if i == 0:
            return self
        elif i > 0:
            element = self
            for j in xrange(i):
                element = element.next()
            return element
        elif i < 0:
            element = self
            for j in xrange(-i):
                element = element.prev()
            return element
        else:
            raise IndexError



# polynomial helpers

def polynomials(field_or_char=0, var='X'):
    if field_or_char == 0:
        field = QQ
    elif isinstance(field_or_char, int):
        field = GF(field_or_char)
    else:
        field = field_or_char
    polynomials = PolynomialRing(field, var)
    return polynomials, gens(polynomials)[0]

QQ_poly, X = polynomials(0, 'X')

def rational_functions(field_or_char=0, var='t'):
    poly, param = polynomials(field_or_char, var)
    field = poly.fraction_field()
    return field, param
