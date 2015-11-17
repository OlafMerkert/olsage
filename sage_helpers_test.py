# -*- coding: utf-8; sage: t -*-

from __future__ import print_function
from sage_helpers import *


def test_latex_strip():
    print(latex_strip(
        "a = -\\frac{1}{3} \\, {\\left(d_{1}^{4} + "
        "2 \\, d_{1}^{2} d_{4}^{2} + d_{4}^{4} - "
        "8 \\, d_{1}^{2} d_{2} + 4 \\, d_{2} d_{4}^{2}"
        " - 12 \\, d_{1} d_{4} d_{5} + 16 \\, d_{2}^{2} +"
        " 12 \\, d_{5}^{2}\\right)} \\mathit{la}^{4} +"
        " \\frac{4}{3} \\, {\\left(d_{1}^{2} + 3 \\, d_{2}^{2} "
        "+ d_{4}^{2} + 3 \\, d_{5}^{2} + 2 \\, d_{2} "
        "+ 3\\right)} \\mathit{la}^{2} - \\frac{16}{3}"))


def test_test_it():
    print(test_it("fail", False, "succeed", True))
    print(test_it("yay", True, "juhu", True))
    print(test_it("oh no", False, "oh my", False, "sh!t", False))


def test_complete_square():
    sq = X**4 + X**2 + 3 * X + 7
    rem = X**3 + X**2 + X
    r = complete_square(ex1**2 + rem)
    print(sq - r[0], rem - r[1])


def test_solve_u_r1():
    m = Matrix([[2, 1, 3],
                [0, 3, 1]])
    v = solve_u_r1(m)
    print(m * v)

def test_quotient_compatible():
    f = quotient_compatible(lambda x, y: (x + y))
    R, X = polynomials(0)
    Rq = R.quotient(ideal(X))
    print("quotient ring {0}".format(Rq))
    r1 = Rq(X + 7)
    r2 = Rq(X**2 + 3 * X + 19)
    print("r1 = {0}, r2 = {1} with parent {2}".format(r1, r2, r1.parent()))
    s1 = r1 + r2
    print("quotient sum {0} with parent {1}".format(s1, s1.parent()))
    s2 = f(r1, r2)
    print("lift sum {0} with parent {1}".format(s2, s2.parent()))

def test_bijection_p():
    bijection_p([[0, 0], [1, 1], [2, 2]]) == True
    bijection_p([[0, 0], [1, 1], [2, 3]]) == False
    bijection_p([[0, 0], [1, 1], [2, 3], [3, 2]]) == True
    bijection_p([[0, 0], [1, 1], [2, 2], [2, 2]]) == False
