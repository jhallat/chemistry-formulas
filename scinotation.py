# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:06:21 2020

@author: John Hallat
"""
from re import match, search

class ScientificNotation:
 
    
    def __init__(self, value):
        self.integral, self.decimal, self.exponent = self.parse(value)        

    def parse(self, value):
        """Parses a string in the form of scientific notation"""
        result = match('-{0,1}[0-9]((\.[0-9]{1,}){0,1}x10\^-{0,1}[0-9]{1,}){0,1}', value)
        if not result:
            raise Exception('Invalid format for scientific notation')

        integral = ''
        decimal = ''
        exponent = ''
        integral_match = search('-{0,1}[0-9]{1,}', value)
        integral = integral_match[0]
        if len(integral) > 1:
            raise Exception('Invalid format for scientific notation')
    
        decimal_match = search('(?<=\.)[0-9]{1,}', value)
        if decimal_match:
            decimal = decimal_match[0]
    
        exponent_match = search('(?<=\^)-{0,1}[0-9]{1,}', value)
        if exponent_match:
            exponent = exponent_match[0]
        
        return (integral, decimal, exponent)  

    
    def sig_digits(self):
        "Determine the amount of signficant digits from scientific notation"
        if self.decimal:
            return len(self.integral) + len(self.decimal)
        else:
            return 1
    




