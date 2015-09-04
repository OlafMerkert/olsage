# -*- coding: utf-8; sage: t -*-

# various essential utility functions for working with sage


# imports
from __future__ import print_function
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
def srepr(item, repr=True):
    if repr and hasattr(item, 'repr'):
        return item.repr()
    else:
        return item


def lrepr(lst, repr=True, ret=False):
    if repr == "table":
        return trepr(lst)
    elif repr:
        for i, l in enumerate(lst):
            print("{0}: {1}".format(i, srepr(l)))
    else:
        for i, l in enumerate(lst):
            print("{0}: {1}".format(i, l))
    if ret:
        return lst


def trepr(lst, repr=True):
    if repr:
        return [[i, srepr(l)] for i, l in enumerate(lst)]
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
            print("\\begin{dmath*}[frame,breakdepth={4}]", latex_strip(latex(a)), "\\end{dmath*}")
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


# degree function useful also for constant polynomials
def degree(poly):
    """Compute the degree of a univariate polynomial or Laurent series."""
    if is_Polynomial(poly):
        return poly.degree()
    elif is_LaurentSeries(poly):
        return poly.valuation()
    else:
        return 0


# completing the square
def sqrt_workaround(number):
    if number == 1:
        return 1
    else:
        return sqrt(number)


def complete_square(poly):
    """we expect an univariate polynomial of even degree, where the
leading coefficient is a square, then we try to find a polynomial
whose square is as close as possible to thte original polynomial."""
    a = poly
    x, = gens(poly.parent())
    deg = poly.degree()
    assert (deg % 2 == 0)
    lc = sqrt_workaround(a[deg])
    b = lc * x ** (deg // 2)
    a -= a[deg] * x ** deg
    for i in xrange(1, deg // 2 + 1, 1):
        c = (a[deg - i] / (2 * lc)) * x ** (deg // 2 - i)
        a -= c * (2 * b + c)
        b += c
    return b, a


def normalise_monic(poly):
    "Make the polynomial or Laurent series monic."
    if is_Polynomial(poly):
        return poly / poly.leading_coefficient()
    elif is_LaurentSeries(poly):
        return poly / poly.coefficients()[0]
    elif poly == 0:
        return 0
    # the final case is a constant polynomial
    else:
        return 1


# Laurent series utilities

# workaround a limitation of sage: it can do sqrt of power series, but not of laurent series.
def laurent_series_sqrt(laurent_series, prec=30):
    val = laurent_series.valuation()
    assert val % 2 == 0
    power_series = laurent_series.shift(-val).power_series()
    return power_series.sqrt(prec=prec).laurent_series().shift(val / 2)

