# -*- coding: utf-8; sage: t -*-

# various essential utility functions for working with sage


# imports
from __future__ import print_function
from sage.all import *
from sage.rings.polynomial.polynomial_element import is_Polynomial
from sage.rings.laurent_series_ring_element import is_LaurentSeries
from sage.rings.polynomial.polynomial_ring import is_PolynomialRing
import re

# wildcards
w = map(SR.wild, xrange(20))


# generating variables
def var_names(base, count):
    """Produce a list of count strings ['base0', 'base1', ...] useful for
    variable names (for polynomials or symbolic variables). See also var_n
    function.
    """
    return [(base + "{0}").format(i) for i in range(count)]

def var_n(base, count):
    """Produce a list of variables with names generated by var_names."""
    names = var_names(base, count)
    if len(names) == 1:
        return [var(names[0])]
    else:
        return list(var(names))


# general utilities
def transpose(list_of_lists):
    """Transpose a list of lists, so a[i][j] becomes a[j][i]. We assume
    that the lists have all the same length."""
    return map(list, zip(*list_of_lists))


def chunks(l, n=2):
    """Given a list, partition it into sublists of uniform length n. If n
    does not divide the length of l, the last sublist may be shorter."""
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

def memoize_instance(f):
    """Method decorator: Memoize a method, by storing the dict with the
    already computed results in a slot of the object. We only memoize
    on the first parameter.
    """
    slot_name = "_m_" + f.__name__

    def m(_self, x, *args):
        if not hasattr(_self, slot_name):
            _self.__dict__[slot_name] = dict()
        if x in _self.__dict__[slot_name]:
            return _self.__dict__[slot_name][x]
        else:
            v = f(_self, x, *args)
            _self.__dict__[slot_name][x] = v
            return v
    return m

def lazy_property(f):
    """
    Method decorator: Turn the given method into a readable property,
    but only do the computation for the first call.
    """
    name = f.__name__
    slot_name = "_" + name

    def m(_self):
        if not hasattr(_self, slot_name):
            _self.__dict__[slot_name] = f(_self)
        return _self.__dict__[slot_name]

    return property(m)


# pretty printing
def srepr(item, repr=True):
    """
    Call repr method on a single object, if it has one. Otherwise just
    the return the object.
    """
    if repr and hasattr(item, 'repr'):
        return item.repr()
    else:
        return item


def lrepr(lst, repr=True, ret=False):
    """
    Print out the elements of lst line by line, with the index at the
    start. If an item has a repr method, print its output instead. If
    repr == 'table', call trepr on lst. Additionally, if ret is True,
    return lst again.
    """
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
    """Like lrepr, but instead of printing items, create a two column
    table with index in the first column, and the object (with repr
    method called if present) in the second. This is useful in
    conjunction with org-babel's :results value table header option.
    """
    if repr:
        return [[i, srepr(l)] for i, l in enumerate(lst)]
    else:
        return [[i, l] for i, l in enumerate(lst)]
    if ret:
        return lst

def fn_labels(repl="", tex=""):
    """A simple decorator to add table headers to functions (or methods),
    which should simplify table building even further.
    """
    def dec(f):
        f.__repl_doc = repl
        f.__tex_doc = tex
        return f
    return dec

def table_builder(header, sep, contents):
    """Produce table output, to be used with org-babel. If sep is True,
    insert a horizontal line before the table body. If header is True,
    insert a header at the top of the table. If header == 'latex', use
    a LaTeX formatted header.

    contents should have the following layout: contents is a list with
    an entry for every column, the entry consisting of a column label,
    a column label for LaTeX output, and a list of the cells in the
    columns (preferably strings, but anything that prints nicely
    should be fine).
    """
    header_list = []
    latex_header_list = []
    body_list = []
    for (label, latex_label, content) in contents:
        if isinstance(label, tuple):
            header_list.extend(label)
            latex_header_list.extend(latex_label)
            body_list.extend(content)
        else:
            header_list.append(label)
            latex_header_list.append(latex_label)
            body_list.append(content)
    sep_list = [["--"] * len(header_list)]
    body_list = zip(*body_list)
    if sep:
        body_list = sep_list + body_list
    if header == "latex":
        body_list = [latex_header_list] + body_list
    elif header:
        body_list = [header_list] + body_list
    return body_list


# producing latex output

produce_latex = True

def latex_strip(string):
    """
    Remove left and right parenthesis groupings, and also the {} around
    them, otherwise the dmath environment fails to perform any
    line-breaking. Also rename the variable la to \\lambda -- we cannot use
    lambda as variable name because it is a keyword.
    """
    string = re.sub("{?\\\\left", "", string)
    string = re.sub("\\\\right\\)}?", ")", string)
    string = re.sub("\\\\mathit{la}", "\\lambda", string)
    return string


def l(*args):
    """
    Format every argument in LaTeX, and put it into a dmath*
    environment (so long formulas may enjoy line breaking). If the global
    variable produce_latex is False, return the arguments instead.
    """
    global produce_latex
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
    def __init__(self, prev=None, next=None, start=0):
        self._prev = prev
        self._next = next
        if prev is not None:
            self._index = prev._index + 1
        else:
            self._index = 0

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
    """Return a univariate PolynomialRing over the given field (or ring),
    and its variable (with given name). Instead of a field, one may
    give a characteristic, in which case the minimal field of said
    characteristic is used as the base.
    """
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
    """Like polynomials, but return  the fraction field instead."""
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
    """Sage has trouble recognising squares or even 1 if we are working
    over a non-trivial base, so we workaround this."""
    if number == 1:
        return 1
    # another trick for symbolic expressions
    elif number.parent() == SR:
        m = number.match(w[0]**2)
        if m:
            return w[0].subs(m)
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


# constructing polynomials

def poly_list(var, lst, reverse=False):
    """Given a variable (or actually any expression) and a list of
    coefficients, produce a polynomial in said variable. The reverse
    options makes the first element of lst the leading coefficient.
    """
    if reverse:
        lst = reversed(lst)
    return sum([var**i * l for i, l in enumerate(lst)])


def random_int_monic_polynomial(deg, limit=80, base=QQ):
    """Return a random polynomial with integer coefficients below limit
    (default 80). The third optional parameter may be use to specify a
    different base than QQ."""
    R, X = polynomials(base)
    poly = randint(0, limit) + X**deg
    for i in xrange(1, deg):
        poly += randint(0, limit) * X**i
    return poly


def poly_over_varlist(varlist):
    """Build a univariate polynomial ring over the domain of definition of
    the elements of varlist (which are assumed to be variables) and return
    its generator."""
    assert len(varlist) > 0
    # to make sure we get the right parent, we do a sum of the variables.
    R, X = polynomials(sum(varlist).parent())
    return X


def monic_free_polynomial(varlist):
    """Return a monic polynomial in X with the coefficients the elements of
    varlist, beginning with the constant coefficient."""
    X = poly_over_varlist(varlist)
    deg = len(varlist)
    poly = X**deg
    for i, v in enumerate(varlist):
        poly += v * X**i
    return poly


def free_polynomial(varlist):
    """Return a polynomial with coefficients the elements of varlist,
    beginning with the constant coefficient."""
    X = poly_over_varlist(varlist)
    return sum([v * X**i for i, v in enumerate(varlist)])

def poly_subs(poly, var, subs):
    """helper function to make polynomials out of symbolic expressions."""
    coeffs = poly.coefficients(var)
    return sum([c[0] * subs**c[1] for c in coeffs])


# Laurent series utilities

def Laurent_series(field_or_char=0, var='Z'):
    """
    The analogue to polynomials. Produce the field of Laurent series
    (in one variable) over a given field (or ring), and return it
    together with the variable (named as desired). Instead of a field,
    one may supply a characteristic, in which case the minimal field
    of said characteristic is used for the base.
    """
    if field_or_char == 0:
        field = QQ
    elif isinstance(field_or_char, int):
        field = GF(field_or_char)
    else:
        field = field_or_char
    laurent_series = LaurentSeriesRing(field, var)
    return laurent_series, gens(laurent_series)[0]


DEFAULT_SERIES_PREC = 30


# workaround a limitation of sage: it can do sqrt of power series, but not of laurent series.
def laurent_series_sqrt(laurent_series, prec=DEFAULT_SERIES_PREC):
    """Compute the sqrt of a Laurent series, by converting it to a power
    series (for which this operation is implemented in sage). This works
    only if the valuation is even. Moreover, if there is a complicated
    leading coefficient involved, this could fail."""
    val = laurent_series.valuation()
    assert val % 2 == 0
    power_series = laurent_series.shift(-val).power_series()
    return power_series.sqrt(prec=prec).laurent_series().shift(val / 2)


def laurent_series_infinity_converter(polynomial_or_ring):
    """
    Given a univariate polynomial in X, we actually want to look at
    Laurent series in X^-1. This function sets up the appropriate
    Laurent series field, and returns a function which converts
    polynomials to Laurent series. The function has the slots target
    and var to access the field and Z = X^-1 directly.
    """
    if is_Polynomial(polynomial_or_ring):
        base = polynomial_or_ring.parent().base_ring()
    elif is_PolynomialRing(polynomial_or_ring):
        base = polynomial_or_ring.base_ring()
    else:
        base = polynomial_or_ring
    L, Z = Laurent_series(base)

    def convert(x):
        if is_Polynomial(x):
            ret = x(1/Z)
            if ret == 1:
                return Integer(1)
            else:
                return ret
        else:
            return x
    convert.target = L
    convert.var = Z
    return convert


def polynomial_laurent_sqrt(polynomial, prec=DEFAULT_SERIES_PREC):
    """
    This computes the sqrt of the polynomial in X as a Laurent series
    in X^-1. The polynomial should have even degree and a not too
    complicated leading coefficient.
    """
    c = laurent_series_infinity_converter(polynomial)
    return laurent_series_sqrt(c(polynomial), prec=prec)


def poly_clear_constants(polynomial_fraction):
    """
    Sage calls reduce on polynomials, but this does not kill common
    constant factors. So we divide both numerator and denominator by
    the common content.
    """
    num_content = polynomial_fraction.numerator().content()
    den_content = polynomial_fraction.denominator().content()
    # this gcd works also for rational expressions.
    g = gcd(num_content, den_content)
    num_new = polynomial_fraction.numerator() / g
    den_new = polynomial_fraction.denominator() / g
    # print("debug num = {0}, den = {1}".format(num_new, den_new))
    return num_new / den_new


def laurent_series_sqrt_with_lc(series, prec=10, lc=None):
    """Use this function to compute a square root of a Laurent series if
    sage cannot figure out what the leading coefficient of the sqrt
    should be -- you may supply it a parameter lc. The prec controls
    how many terms are computed, however be aware that the result
    might have the wrong O(X^n) term if the argument is not a
    polynomial (i.e. already has an O(X^m) term).
    """
    T, = series.parent().gens()
    v = series.valuation()
    assert v % 2 == 0

    def c(n):
        return series[v + n]

    b = []
    if lc is None:
        lc = sqrt(c(0))

    b.append(lc)

    for k in range(1, prec):
        # don't optimise the sum yet, it might make trouble
        s = c(k) - sum([b[i] * b[k-i] for i in range(1, k)])
        b.append(poly_clear_constants(s/(2*lc)))

    return O(T**(v//2 + prec)) + sum([b_n * T**(v//2 + i) for (i, b_n) in enumerate(b)])


# various utilities for working with the symbolic ring

def dsolve(expr, var):
    """Abbreviation so solve spits out a dictionary instead of (useless)
    equations."""
    return solve(expr, var, solution_dict=True)


def subs_map(lst, *sbs):
    """Apply the substitutions for every item in lst."""
    return [l.subs(*sbs) for l in lst]


def subs_n(expr, *sbs):
    """Apply the given substitutions one after the other on the expression."""
    for s in sbs:
        expr = expr.subs(s)
    return expr


def subs_nmap(lst, *sbs):
    """Apply the given substitutions one after the other for every item in lst."""
    return [subs_n(l, *sbs) for l in lst]


def factor0(expr):
    """Instead of producing an error message when factoring 0, just return
    0. This is very useful in conjunction with map or list
    comprehensions."""
    if expr == 0:
        return 0
    else:
        return factor(expr)


def psolve(polys, variables, solution_field=None):
    """
    Given a list of polynomials and variables, solve the equations poly
    = 0 for the variables. Return a dictionary with the solutions, if any
    are found.
    """
    if solution_field is None:
        solution_field = polys[0].parent().fraction_field()
    sp = map(SR, polys)
    sv = map(SR, variables)
    ssol = dsolve(sp, sv)
    # print("debug solutions {0}".format(ssol))
    psol = []
    for sol in ssol:
        psl = map(solution_field, subs_map(sv, sol))
        psol.append({x: y for (x, y) in zip(variables, psl)})
    return psol

def num_simpl(x):
    """
    Take the numerator of an expression, and divide by its content.
    This produces the minimal equation required to solve, if we want
    some rational function to vanish.
    """
    n = x.numerator()
    c = n.content()
    return n/c

def eq_resolve(co, var, choice=0, full=True):
    """
    Take the len(var) first equations in co, and solve them for
    everything in var, the resubstitute the solution selected by
    choice into the equations, and unless full==False, full_simplify
    the results. Return the solution_dict and the still to be solved
    equations.
    """
    l = len(var)
    if l == 1:
        var = var[0]
    print("debug l = {0}".format(l))
    sol = dsolve(co[:l], var)
    print(sol)
    simpm = lambda x: x.full_simplify()
    co_solved = map(simpm, subs_map(co[:l], sol[choice]))
    print(co_solved)
    if full is None:
        simpm = lambda x: x
    elif not full:
        simpm = lambda x: x.simplify()
    co_new = map(simpm, subs_map(co[l:], sol[choice]))
    lrepr(co_new)
    return sol, co_new


def eq_replace(co, s, full=True):
    """
    Allow manual substitution into a list of equations, with the same
    interface as eq_resolve.
    """
    if full:
        simpm = lambda x: x.full_simplify()
    else:
        simpm = lambda x: x.simplify()
    co_new = [simpm(x.subs(s)) for x in co]
    lrepr(co_new)
    return s, co_new


def eq_from_coeff(expr, v, start, end):
    assert start <= end
    return [x[0] for x in expr.coefficients(v) if start <= x[1] < end]


# linear terms in polynomials
linear_terms_variables = []

def linear_terms(expr):
    """
    List all elements of linear_terms_variables which appear only as a
    linear term in expr.
    """
    return [v for v in linear_terms_variables if expr.degree(v) == 1]

def linear_term_complexity(expr, v):
    """
    For a given variable, compute the complexity of its linear
    coefficient by counting variables appearing in it.
    """
    mons = expr.coefficient(v).monomials()
    return sum([x.degree() for x in mons])

def linear_term_complexity_chart(expr):
    """
    Produce a list of the variables appearing as linear term in expr,
    sorted by the complexity of their coefficient.
    """
    lt = linear_terms(expr)
    ltc = [[l, linear_term_complexity(expr, l)] for l in lt]
    ltc.sort(key=lambda x: x[1])
    return ltc
