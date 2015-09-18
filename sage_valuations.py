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
    R = field.ring_of_integers()
    I = R.ideal(uniformiser)
    return R.quotient(I)


def reduced_polynomials(field_or_polynomial_ring, uniformiser):
    if isinstance(field_or_polynomial_ring, PolynomialRing):
        field = field_or_polynomial_ring.parent()
    else:
        field = field_or_polynomial_ring
    return polynomials(residue_field(field, uniformiser), 'Y')[0]
