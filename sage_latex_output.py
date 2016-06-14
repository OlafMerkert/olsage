# -*- coding: utf-8; sage: t -*-

# A number of helper functions for outputting tuned latex code. Unlike
# the l function in sage_helpers which aims at convenient export of
# computational org files, these are more intended for controlled
# output to be included in publications.


# imports
from __future__ import print_function
from sage.all import (QQ,
                      latex,
                      lcm,
                      factor)
from sage_helpers import (latex_strip,
                          is_Polynomial)
from sage.rings.number_field.number_field import is_NumberField
from sage.rings.fraction_field import is_FractionField
from sage.rings.polynomial.polynomial_ring import is_PolynomialRing


# basic latex output

def ll_raw(*stuff):
    """For each argument, generate a latex representation, unless the
    argument is already a string. Superfluous curly braces and \\left
    or \\right commands are removed. Moreover, the variable la is
    replaced by lambda."""
    result = ""
    for s in stuff:
        if isinstance(s, basestring):
            result += s
        else:
            result += latex_strip(latex(s))
    return result

def ll(*stuff):
    """Generate inline math formula, wrapping ll_raw."""
    return "\\(" + ll_raw(*stuff) + "\\)"

def lle(*stuff):
    """Generate display math formula, wrapping ll_raw."""
    return "\\[" + ll_raw(*stuff) + "\\]"

def lleq(*stuff):
    "Generate equation math formula, wrapping ll_raw."
    return "\\begin{equation}\n" + ll_raw(*stuff) + "\\end{equation}\n"

def commas(l, sep=", "):
    """Given a list and a separator, construct a new list with the
    separator inserted between all the previous list elements. There
    is no final separator at the end, the default is ', '."""
    r = []
    for i in l:
        r.append(i)
        r.append(sep)
    return r[:-1]

def ll_common_denominator(f):
    """For a polynomial f with fractional coefficients, write out the
    polynomial such that there is only a single denominator."""
    # f should be a polynomial
    if not is_Polynomial(f):
        return ll_raw(f)
    # first determine the lcm of the denominators of the coefficients
    cd = reduce(lcm, [c.denominator() for c in f])
    if is_Polynomial(cd) and cd.degree() > 0:
        return "\\frac{" + ll_raw(cd * f) + "}{" + ll_raw(factor(cd)) + "}"
    else:
        return ll_raw(f)


# formatting various standard sage objects

class UnknownField():
    pass

def field_format(field):
    """Print a nice representation of the given field object. This works
    correctly for number fields, but for fraction fields of polynomial
    rings we just pretend the base field are the complex numbers (for
    now)."""
    # print("debug field = {0}".format(field))
    if field == QQ:
        return ll("\\Q")
    elif is_NumberField(field):
        minpoly = field.defining_polynomial()
        g, = field.gens()
        # G, = minpoly.parent().gens()
        return (ll("K = \\Q(", g, ")") + ", where " +
                ll(g) + " has minimal polynomial " + ll(minpoly))
    elif is_FractionField(field):
        ring = field.ring_of_integers()
        if is_PolynomialRing(ring):
            return ll("\\C(", ring.gens()[0], ")")
        else:
            print("debug ring =  {0}".format(ring))
            raise UnknownField()
    else:
        raise UnknownField()
