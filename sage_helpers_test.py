# -*- coding: utf-8; sage: t -*-


def test_latex_strip():
    print latex_strip(
        "a = -\\frac{1}{3} \\, {\\left(d_{1}^{4} + "
        "2 \\, d_{1}^{2} d_{4}^{2} + d_{4}^{4} - "
        "8 \\, d_{1}^{2} d_{2} + 4 \\, d_{2} d_{4}^{2}"
        " - 12 \\, d_{1} d_{4} d_{5} + 16 \\, d_{2}^{2} +"
        " 12 \\, d_{5}^{2}\\right)} \\mathit{la}^{4} +"
        " \\frac{4}{3} \\, {\\left(d_{1}^{2} + 3 \\, d_{2}^{2} "
        "+ d_{4}^{2} + 3 \\, d_{5}^{2} + 2 \\, d_{2} "
        "+ 3\\right)} \\mathit{la}^{2} - \\frac{16}{3}")


def test_test_it():
    print test_it("fail", False, "succeed", True)
    print test_it("yay", True, "juhu", True)
    print test_it("oh no", False, "oh my", False, "sh!t", False)
