import unittest
from scinotation import Scinot


def test_parse_full():
    number = Scinot('2.33x10^23')
    assert '2' == number._integral
    assert '33' == number._decimal
    assert '23' == number._exponent

def test_parse_small_decimal():
    number = Scinot('0.0120')
    assert '1' == number._integral
    assert '20' == number._decimal
    assert '-2' == number._exponent

def test_multiplication():
    number_one = Scinot('2.44x10^2')
    number_two = Scinot('3.1x10^1')
    product = number_one * number_two
    assert '7' == product._integral
    assert '6' == product._decimal
    assert '3' == product._exponent

def test_equals():
    number_one = Scinot('1.54x10^2')
    number_two = Scinot('1.54x10^2')
    assert number_one == number_two

def test_not_equals():
    number_one = Scinot('1.54x10^2')
    number_two = Scinot('1.53x10^2')
    assert number_one != number_two

def test_subtraction():
    number_one = Scinot('5.00x10^0')
    number_two = Scinot('2.61x10^0')
    number_three = Scinot('6.57x10^-1')
    actual = number_one - number_two - number_three
    expected = Scinot('1.73x10^0')
    assert expected == actual

