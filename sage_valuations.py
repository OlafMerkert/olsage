# -*- coding: utf-8; sage: t -*-

from __future__ import print_function
from sage_helpers import *


# computing Gauss norms

def gauss_valuation(poly, prime, prec=30):
    """Compute the Gauss norm of the given polynomial, with prime
    identifying the valuation."""
    if is_Polynomial(poly):
        return min([valuation(c, prime) for c in poly])
    if is_LaurentSeries(poly):
        return series_valuation(poly, prime, prec)
    else:
        # in case we just get a constant
        return valuation(poly, prime)


def series_valuation(series, prime, prec=30):
    """Compute the Gauss norm of the given Laurent series, with prime
    identifying the valuation. For practical reasons, we use a simple
    heuristic to determine if this valuation is bounded: We look at
    prec terms, and unless the minimal valuation occurs in the first
    two thirds of these, we say that we have unbounded valuation."""
    assert is_LaurentSeries(series)
    deg = series.valuation()
    trunc = series.truncate(prec - deg)
    coeffs = [valuation(c, prime) for c in list(trunc)]
    allmin = apply(min, coeffs)
    end = (2 * len(coeffs)) // 3
    startmin = apply(min, coeffs[:end])
    if startmin > allmin:
        return -infinity
    else:
        return allmin


def normalise_for_prime(prime, *polys):
    """Normalise the given polynomial (or Laurent series) so that it has valuation 0."""
    exponent = min([gauss_valuation(poly, prime) for poly in polys])
    f = prime**(-exponent)
    if len(polys) == 1:
        return f * polys[0]
    else:
        return [f * poly for poly in polys] + [exponent]


# domain operations

# residue field and related
def residue_field(field, uniformiser):
    """
    Given a field, and a prime in its ring of integers, return the corresponding residue field.
    """
    R = field.ring_of_integers()
    I = R.ideal(uniformiser)
    return R.quotient(I)


def reduced_polynomials(field_or_polynomial_ring, uniformiser, var_name='Y'):
    """Given a univariate polynomial ring, take the residue field wrt the uniformiser and return a univariate polynomial ring over it."""
    if is_PolynomialRing(field_or_polynomial_ring):
        field = field_or_polynomial_ring.base_ring()
    else:
        field = field_or_polynomial_ring
    return polynomials(residue_field(field, uniformiser), var_name)[0]


# projective and affine heights, also for polynomials

def first_poly2vector(f):
    """
    A decorator: If the first argument for the function f is a
    polynomial, invoke f with the list of coefficients instead. This make
    any projective or affine height accept also polynomials.
    """
    def m(poly_or_vector, *args):
        if is_Polynomial(poly_or_vector):
            return f(poly_or_vector.coefficients(), *args)
        else:
            return f(poly_or_vector, *args)
    return m

@first_poly2vector
def projective_height(vector, abs_val=lambda x: x.abs()):
    """The projective exponential height function (works only over the rationals?)."""
    denoms = [v.denominator() for v in vector]
    nums = [v.numerator() for v in vector]
    d = lcm(denoms)
    g = gcd(nums)
    return abs_val(d)/abs_val(g) * max([abs_val(v) for v in vector])

@first_poly2vector
def projective_global_height(vector, abs_val=lambda x: x.abs()):
    """The projective logarithmic height function (works only over the rationals?)."""
    # use .numerical_approx() if we want a float
    return log(projective_height(vector, abs_val))

@first_poly2vector
def affine_height(vector, abs_val=lambda x: x.abs()):
    """The affine exponential height function (works only over the rationals?)."""
    return projective_height(list(vector) + [Integer(1)], abs_val)

@first_poly2vector
def affine_global_height(vector, abs_val=lambda x: x.abs()):
    """The affine logarithmic height function (works only over the rationals?)."""
    # use .numerical_approx() if we want a float
    return log(affine_height(vector, abs_val))
