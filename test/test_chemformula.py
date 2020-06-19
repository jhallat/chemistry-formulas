from decimal import Decimal

from src.chemistry.chemformula import composition, Component, formula_from_percent, formula_from_mass, \
    mol_formula_from_simple_formula, predict_formula, compound_name
from src.chemistry.measurement import grams
from src.chemistry.scinotation import Scinot


def test_composition_NaHCO3():
    actual = composition('NaHCO3')
    expected = Component(1, 'Na', grams('0.2737'), Decimal('27.37'))
    assert expected == actual[0]
    expected = Component(1, 'H', grams('0.01200'), Decimal('1.20'))
    assert expected == actual[1]
    expected = Component(1, 'C', grams('0.1430'), Decimal('14.30'))
    assert expected == actual[2]
    expected = Component(3, 'O', grams('0.5714'), Decimal('57.14'))
    assert expected == actual[3]


def test_composition_CO2():
    actual = composition('CO2')
    expected = Component(1, 'C', grams('0.2729'), Decimal('27.29'))
    assert expected == actual[0]
    expected = Component(2, 'O', grams('0.7271'), Decimal('72.71'))
    assert expected == actual[1]


def test_amount_of_iron_in_limonite():
    actual = composition('Fe2O3*[3/2]H2O', grams(Scinot('1.0000x10^6')))
    expected = Component(2, 'Fe', grams(Scinot('5.9820x10^5')), Decimal('59.82'))
    assert expected == actual[0]


def test_formula_of_Sn_and_O():
    elements = [('Sn', Decimal('78.8')),
                ('O', Decimal('21.2'))]
    actual = formula_from_percent(elements)
    expected = "SnO2"
    assert expected == actual


def test_formula_of_K_Cr_O():
    elements = [('K', Decimal('26.6')),
                ('Cr', Decimal('35.4')),
                ('O', Decimal('38.0'))]
    actual = formula_from_percent(elements)
    expected = "K2Cr2O7"
    assert expected == actual


def test_formula_of_C_H_O():
    elements = [('C', grams('2.61')),
                ('H', grams('0.658')),
                ('O', grams('1.73'))]
    actual = formula_from_mass(elements)
    expected = "C2H6O"
    assert expected == actual

def test_mol_formula_of_vitamin_c():
    actual = mol_formula_from_simple_formula("C3H4O3", Decimal('180'))
    expected = "C6H8O6"
    assert expected == actual

def test_predict_lithium_and_oxygen():
    actual = predict_formula('Li + O')
    expected = 'Li2O'
    assert expected == actual

def test_predict_chlorine_and_magnesium():
    actual = predict_formula('Cl + Mg')
    expected = 'MgCl2'
    assert expected == actual

def test_predict_nickel_and_sulfur():
    actual = predict_formula(['Ni', 'S'])
    expected = 'NiS'
    assert expected == actual

def test_predict_barium_and_hydroxide():
    actual = predict_formula('Ba + OH')
    expected = 'Ba(OH)2'
    assert expected == actual

def test_predict_potassium_and_sulfate():
    actual = predict_formula(['SO4', 'K'])
    expected = 'K2SO4'
    assert expected == actual

def test_predict_ammonium_and_phosphate():
    actual = predict_formula('NH4 + PO4')
    expected = '(NH4)3PO4'
    assert expected == actual

def test_predict_zinc_and_silver():
    actual = predict_formula('Zn + Ag')
    expected = 'Zn + Ag'
    assert actual == expected

def test_predict_barium_hydroxide():
    actual = predict_formula('barium hydroxide')
    expected = 'Ba(OH)2'
    assert actual == expected

def test_predict_pottasium_sulfate():
    actual = predict_formula('potassium sulfate')
    expected = 'K2SO4'
    assert actual == expected

def test_predict_ammonium_phosphate():
    actual = predict_formula('ammonium phosphate')
    expected = '(NH4)3PO4'
    assert actual == expected

def test_predict_dinitrogen_pentoxide():
    actual = predict_formula('dinitrogen pentoxide')
    expected = 'N2O5'
    assert actual == expected

def test_predict_H2O():
    actual = predict_formula('water')
    expected = 'H2O'
    assert actual == expected

def test_compound_name_NaCl():
    actual = compound_name('NaCl')
    expected = 'sodium chloride'
    assert actual == expected

def test_compound_name_K2SO4():
    actual = compound_name('K2SO4')
    expected = 'potassium sulfate'
    assert actual == expected

def test_compound_name_Zn_NO3_2():
    actual = compound_name('Zn(NO3)2')
    expected = 'zinc nitrate'
    assert actual == expected

def test_compound_name_FeCl2():
    actual = compound_name('FeCl2')
    expected = 'iron(II) chloride'
    assert actual == expected

def test_compound_name_Al_NO3_3():
    actual = compound_name('Al(NO3)3')
    expected = 'aluminum nitrate'
    assert actual == expected

def test_compound_name_SO2():
    actual = compound_name('SO2')
    expected = 'sulfur dioxide'
    assert actual == expected

def test_compound_name_N2O5():
    actual = compound_name('N2O5')
    expected = 'dinitrogen pentoxide'
    assert actual == expected

def test_compound_name_H2O():
    actual = compound_name('H2O')
    expected = 'water'
    assert actual == expected

def test_compound_name_HCl_gas():
    actual = compound_name('HCl(g)')
    expected = "hydrogen chloride"
    assert actual == expected

def test_compound_name_HCl_aqueous():
    actual = compound_name('HCl(aq)')
    expected = "hydrochloric acid"
    assert actual == expected