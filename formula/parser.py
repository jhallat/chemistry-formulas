from collections import namedtuple
from decimal import Decimal
from enum import Enum

from formula.tokenizer import FormulaToken, FormulaTokenType, tokenize
from periodictable import Ions
from scinotation import Count


class FormulaParseError(Exception):
    pass

class FormulaNodeType(Enum):
    COMPOUND = 0
    ATOM = 1
    MONATOMIC_ION = 2
    POLYATOMIC_ION = 3

class ParseState(Enum):
    START = 1
    COEFFICIENT = 2
    SYMBOL = 3
    SUBSCRIPT = 4

class FormulaRoot:

    def __init__(self, symbol, children):
        self.symbol = symbol
        self.children = children

    def __eq__(self, other):
        if isinstance(other, FormulaRoot):
            return self.symbol == other.symbol and self.children == other.children

    def __repr__(self):
        return f"formula_root(symbol='{self.symbol},children={self.children}'"

    def __getitem__(self, item):
        return self.children[item]

    def flatten(self):
        atoms = []
        for compound in self.children:
            atoms += self._flatten_compound(compound.count, compound.children)

        atom_map = {}
        for atom in atoms:
            atom_sum = atom_map.get(atom[1], Count(0))
            atom_sum += atom[0]
            atom_map[atom[1]] = atom_sum

        return [(value, key) for key, value in atom_map.items()]

    def _flatten_compound(self, count, compound):

        atoms = []
        for node in compound:
            if node.type == FormulaNodeType.ATOM:
                atoms.append((node.count * count, node.symbol))
            else:
                atoms += self._flatten_compound(node.count, node.children)
        return atoms

#TODO need to convert to a class and implement __eq__
FormulaNode = namedtuple("formula_node", "count symbol type children")



def _reduce(elements: [(Decimal, str)]) -> [(Decimal, str)]:
    element_map = {}
    reduced_elements = []
    for element in elements:
        amount = element_map.get(element[1], Decimal(0.000))
        amount += element[0]
        element_map[element[1]] = amount

    for element in elements:
        if element[1] in element_map:
            reduced_elements.append((element_map.pop(element[1]), element[1]))

    return reduced_elements

def state_state(index, token, coefficient, symbol, polyatomic):
    if token.type == FormulaTokenType.COEFFICIENT:
        coefficient = Decimal(token.value)
        state = ParseState.COEFFICIENT
    elif token.type == FormulaTokenType.SYMBOL:
        symbol = token.value
        state = ParseState.SYMBOL
    elif token.type == FormulaTokenType.SUBSCRIPT and polyatomic:
        coefficient = Decimal(token.value)
        state = ParseState.COEFFICIENT
    else:
        raise FormulaParseError(f"unexpected token '{token.value}' at index {index}, expected coefficient or symbol")
    return coefficient, symbol, state

def state_coefficient(index, token):
    if token.type == FormulaTokenType.SYMBOL:
        symbol = token.value
        state = ParseState.SYMBOL
    else:
        raise FormulaParseError(f"unexpected token '{token.value}' at index {index}, expected symbol")
    return symbol, state

def state_symbol(index, token, coefficient, symbol, atoms, compound):
    if token.type == FormulaTokenType.SYMBOL:
        atoms.append(FormulaNode(Count(1), symbol, FormulaNodeType.ATOM, []))
        compound += symbol
        symbol = token.value
        state = ParseState.SYMBOL
    elif token.type == FormulaTokenType.SUBSCRIPT:
        atoms.append(FormulaNode(Count(token.value), symbol, FormulaNodeType.ATOM, []))
        compound += symbol + token.value
        symbol = ''
        state = ParseState.SUBSCRIPT
    else:
        raise FormulaParseError(f"unexpected token '{token.value}' at index {index}, expected symbol, subscript or '*'")
    return coefficient, symbol, atoms, compound, state

def state_subscript(index, token):
    if token.type == FormulaTokenType.SYMBOL:
        symbol = token.value
        state = ParseState.SYMBOL
    else:
        raise FormulaParseError(f"unexpected token '{token.value}' at index {index}, expected symbol or '*'")
    return symbol, state

def _parse_pass_two(tokens: [FormulaToken], polyatomic = False):

    atoms = []
    state = ParseState.START
    coefficient = Decimal('1.000')
    symbol = ''
    compound = ''

    for index, token in enumerate(tokens):
        if state == ParseState.START:
            if isinstance(token, list):
                atoms.append(_parse_pass_two(token, True))
            else:
                coefficient, symbol, state = state_state(index, token, coefficient, symbol, polyatomic)

        elif state == ParseState.COEFFICIENT:
            if isinstance(token, list):
                atoms.append(_parse_pass_two(token, True))
            else:
                symbol, state = state_coefficient(index, token)
        
        elif state == ParseState.SYMBOL:
            if isinstance(token, list):
                atoms.append(FormulaNode(Count(1), symbol, FormulaNodeType.ATOM, []))
                ion = _parse_pass_two(token, True)
                atoms.append(ion)
                compound += symbol
                symbol = ''
                if ion.count > 1:
                    compound += f'({ion.symbol}){str(ion.count)}'
                else:
                    compound += ion.symbol
            else:
                coefficient, symbol, atoms, compound, state =\
                    state_symbol(index, token, coefficient, symbol, atoms, compound)
        
        elif state == ParseState.SUBSCRIPT:
            if isinstance(token, list):
                ion = _parse_pass_two(token, True)
                atoms.append(ion)
                if ion.count > 1:
                    compound += f'({ion.symbol}){str(ion.count)}'
                else:
                    compound += ion.symbol
            else:
                symbol, state = state_subscript(index, token)
        else:
            raise FormulaParseError(f"unexpected state '{state}")    

    if len(symbol) > 0 and state == ParseState.SYMBOL:
        compound += symbol
        atoms.append(FormulaNode(Count(1), symbol, FormulaNodeType.ATOM, []))

    if polyatomic:
        return FormulaNode(Count(coefficient), compound, FormulaNodeType.POLYATOMIC_ION, atoms)
    else:
        return FormulaNode(Count(coefficient), compound, FormulaNodeType.COMPOUND, atoms)

def _parse_pass_one(tokens):

    COMPOUND = 0
    POLYATOMIC = 1
    POLYATOMIC_END = 2

    root = []
    compound = []
    polyatomic = []
    state = COMPOUND
    for token in tokens:
        if token.type == FormulaTokenType.COMBINDED_WITH:
            root.append(compound)
            compound = []
        if token.type == FormulaTokenType.POLYATOMIC_START:
            state = POLYATOMIC
        if token.type == FormulaTokenType.POLYATOMIC_END:
            state = POLYATOMIC_END
        if token.type == FormulaTokenType.COEFFICIENT:
            if state == COMPOUND:
                compound.append(token)
            if state == POLYATOMIC:
                polyatomic.append(token)
            if state == POLYATOMIC_END:
                compound.append(polyatomic)
                compound.append(token)
                polyatomic = []
                state = COMPOUND
        if token.type == FormulaTokenType.SUBSCRIPT:
            if state == COMPOUND:
                compound.append(token)
            if state == POLYATOMIC:
                polyatomic.append(token)
            if state == POLYATOMIC_END:
                polyatomic.insert(0, token)
                compound.append(polyatomic)
                polyatomic = []
                state = COMPOUND
        if token.type == FormulaTokenType.SYMBOL:
            if state == COMPOUND:
                compound.append(token)
            if state == POLYATOMIC:
                polyatomic.append(token)
            if state == POLYATOMIC_END:
                compound.append(polyatomic)
                polyatomic = []
                compound.append(token)
                state = COMPOUND
    if polyatomic:
        compound.append(polyatomic)
    root.append(compound)
    return root


#TODO add a precision parameter for multiply coefficient with subscript. Default = 3
def parse_formula(formula: str):

    tokens = tokenize(formula)
    print(tokens)
    root = _parse_pass_one(tokens)
    print(root)
    children = [_parse_pass_two(compound) for compound in root]
    return FormulaRoot(formula, children)


def parse_ion_equation(equation: str):

    ions = Ions()
    parts = equation.split('->')
    if '+' in parts[0]:
        reactants = [ions[reactant.strip()] for reactant in parts[0].split('+')]
    else:
        reactants = [ions[reactant.strip()] for reactant in parts[0].split()]
    return reactants


