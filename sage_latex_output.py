# -*- coding: utf-8; sage: t -*-

# A number of helper functions for outputting tuned latex code. Unlike
# the l function in sage_helpers which aims at convenient export of
# computational org files, these are more intended for controlled
# output to be included in publications.


# imports
from __future__ import print_function
from sage.all import (latex)
from sage_helpers import latex_strip


# basic latex output

def ll_raw(*stuff):
    result = ""
    for s in stuff:
        if isinstance(s, basestring):
            result += s
        else:
            result += latex_strip(latex(s))
    return result

def ll(*stuff):
    return "\\(" + ll_raw(*stuff) + "\\)"

def lle(*stuff):
    return "\\[" + ll_raw(*stuff)+ "\\]"

def lleq(*stuff):
    return "\\begin{equation}\n" + ll_raw(*stuff)+ "\\end{equation}\n"

def commas(l, sep=", "):
    r = []
    for i in l:
        r.append(i)
        r.append(sep)
    return r[:-1]

def ll_common_denominator(f):
    # f should be a polynomial
    if not is_Polynomial(f):
        return ll_raw(f)
    # first determine the lcm of the denominators of the coefficients
    cd = reduce(lcm, [c.denominator() for c in f])
    if is_Polynomial(cd) and cd.degree() > 0:
        return "\\frac{" + ll_raw(cd * f) + "}{" + ll_raw(factor(cd)) + "}"
    else:
        return ll_raw(f)
