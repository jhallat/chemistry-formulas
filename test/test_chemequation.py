from chemistry.chemequation import parse_equation

def test_parse_N2H_N2O4():
    parse_equation('N2H4 + N2O4 -> N2 + H2O')