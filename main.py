'''
Student Name: Hareeshan Elankeeran
Student ID: 52103699
README:
A program that converts an expression, inputted as a string, into a binary tree.
To run the tests, input Y as your answer to the question. To use the program, type N. The code to generate the tree is taken from the Data Structures and Algorithms in Python Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser John Wiley & Sons, 2013 book, from the GitHub repository https://github.com/mjwestcott/Goodrich.  '''

import operator as op
import pickle
import unittest
from tree import build_expression_tree, tokenize


class Expression:
    '''An Expression class, which takes in either an integer between 0-9 as the operands, or another instance of the expression class, as well as the operator.'''

    def __init__(self, operand1, operator, operand2):
        self.operator = operator
        if isinstance(operand1, Expression):
            self.X = operand1.evaluate()
        else:
            self.X = operand1
        if isinstance(operand2, Expression):
            self.Y = operand2.evaluate()
        else:
            self.Y = operand2
        if operator == '+':
            self.operation = op.add
        elif operator == '-':
            self.operation = op.sub
        elif operator == '/':
            self.operation = op.truediv
            # remember to validate divisions.
            if operand2 == 0:
                raise ZeroDivisionError(
                    'Operand cannot be zero / evaluate to zero.')
        elif operator == '*':
            self.operation = op.mul

        self.type = (type(operand1), type(operand2))

    def evaluate(self):
        'Evaluates the operation in the instance.'
        try:
            return self.operation(self.X, self.Y)
        except ArithmeticError:
            print('Error')


class ArrayStack:
    '''LIFO Stack implementation using a Python list as underlying storage. Taken from the Goodrich Data Structures and Algorithms in Python book, Chapter 6.'''

    def __init__(self):
        '''Create an empty stack.'''
        self.data = []
        # nonpublic list instance

    def __len__(self):
        '''Return the number of elements in the stack.'''
        return len(self. data)

    def isempty(self):
        '''Return True if the stack is empty.'''
        return len(self. data) == 0

    def push(self, e):
        '''Add element e to the top of the stack.'''
        self.data.append(e)  # new item stored at end of list

    def top(self):
        '''Return (but do not remove) the element at the top of the stack.
        Raise Empty exception if the stack is empty. '''
        if self.isempty():
            return False
        return self.data[-1]
# the last item in the list

    def pop(self):
        '''Remove and return the element from the top of the stack (i.e., LIFO).
        Raise Empty exception if the stack is empty. '''
        if self.isempty():
            return False
        return self.data.pop()  # remove last item from list

    def empty(self):
        '''Clears the stack.'''
        self.data = []


class Parser:
    def __init__(self):
        '''Create an empty parser.'''

        self.input = ''
        self.expressions = ArrayStack()
        self.originalstring = ''

    def parseString(self, expression_string, original=False):
        'Parses an expression written as a string. Takes in the expression as a string, and a boolean value, to know if it is at the start of the recursion or not.'
        if original is True:
            self.originalstring = expression_string

        # removes whitespace from string.
        self.input = expression_string.replace(" ", "")
        self.bracketStack = ArrayStack()
        self.operatorStack = ArrayStack()
        operators = ['+', '-', '*', '/']
        for character in range(len(self.input)):
            if self.input[character] == '(':
                self.bracketStack.push(character)
            elif self.input[character] == ')':
                self.bracketStack.push(character)
            if self.input[character] in operators:
                # get the indexes of the operators.
                self.operatorStack.push(character)

        # print(self.operatorStack.data)

        if self.validateString() is True:
            # Parsing of the expression.
            for i in self.bracketStack.data:
                for j in self.bracketStack.data:
                    if i != j and abs(i-j) > 2 and i < j:
                        valid = self.input[i:j+1]
                        if '(' in valid and ')' in valid:
                            operatorloc = [x for x in range(len(valid)) if valid[x] in [
                                '+', '-', '*', '/']]
                            op1 = valid[1:operatorloc[0]]
                            op2 = valid[operatorloc[0]+1: -1]
                            if abs(i-j) >= 4 and len(operatorloc) == 1 and (op1.isdigit() is True and op2.isdigit() is True):
                                #print('Shortest expression = ', valid)
                                e = Expression(
                                    int(op1), valid[operatorloc[0]], int(op2))
                                output = e.evaluate()

                                if len(self.bracketStack) > 2:
                                    return self.parseString(self.input.replace(valid, str(output)))
                                return output
                        else:
                            pass

    def validateString(self):
        '''Validates the expression currently stored in the original string.'''
        if len(self.bracketStack) % 2 != 0:
            raise BracketMismatchError(
                'Not a valid expression, brackets mismatched.')
        elif len(self.operatorStack) < len(self.bracketStack) / 2:
            raise MissedOperatorError(
                'Not a valid expression, operator missing.')
        elif len(self.operatorStack) != len(self.bracketStack) / 2:
            raise OperandError(
                'Not a valid expression, wrong number of operands.')
        else:
            return True

    def createExpressionTree(self):
        '''Creates the expression tree.'''
        token = tokenize(self.originalstring)
        newTree = build_expression_tree(token)
        return newTree

    def displayTree(self):
        '''Displays the binary tree, as a list.'''
        binary_tree = self.createExpressionTree()
        treelist = []
        for i in binary_tree.positions():
            treelist.append(binary_tree.depth(i) * '  ' + str(i.element()))
        return treelist

    def pickleTree(self, binary_tree):
        '''Saves the binary tree list using the pickle module.'''
        try:
            filename = str(input('Please enter a filename: '))
            file = open(filename, 'wb')
            pickle.dump(binary_tree, file)
            file.close()
            print('File saved.')
            return True
        except:
            raise MiscError('There was an error with the file.')

    def loadTree(self):
        '''Loads the tree list, from a file. '''
        try:
            filename = str(input('Please enter a filename: '))
            file = open(filename, 'rb')
            saved = pickle.load(file)
            file.close()
            return saved
        except:
            raise MiscError('File does not exist, or file cannot be opened.')


class OperandError(Exception):
    '''An error class, derived from the Exception class.'''
    pass


class BracketMismatchError(Exception):
    '''Raised if the brackets on a string are mismatched, derived from the Exception class.'''
    pass


class MissedOperatorError(Exception):
    '''Raised if there is an operator missing, derived from the Exception class.'''
    pass


class MiscError(Exception):
  '''A miscellaneous error. '''
  pass
class Testing(unittest.TestCase):
    '''The testing class. This handles all unit tests. Uses the unittest module. '''

    '''Testing if errors are thrown, when the validateString method is used in the Parser class.'''
    def test_wrongoperand1(self):
        self.testParser = Parser()
        with self.assertRaises(OperandError):
            self.testParser.parseString('(4*3*2)', True)

    def test_wrongoperand2(self):
        self.testParser = Parser()
        with self.assertRaises((OperandError, MissedOperatorError)):
            self.testParser.parseString('(4*(2))', True)

    def test_wrongoperand3(self):
        self.testParser = Parser()
        with self.assertRaises(OperandError):
            self.testParser.parseString('(4*(3+2)*(2+1))', True)

    def test_bracketmismatch1(self):
        self.testParser = Parser()
        with self.assertRaises((BracketMismatchError, OperandError)):
            self.testParser.parseString('(2*4)*(3+2)', True)

    def test_bracketmismatch2(self):
        self.testParser = Parser()
        with self.assertRaises(BracketMismatchError):
            self.testParser.parseString('((2+3)*(4*5)', True)

    def test_bracketmismatch3(self):
        self.testParser = Parser()
        with self.assertRaises(BracketMismatchError):
            self.testParser.parseString('(2+5)*(4/(2+2)))', True)

    def test_operator1(self):
        self.testParser = Parser()
        with self.assertRaises(MissedOperatorError):
            self.testParser.parseString('(((2+3)*(4*5))+(1(2+3)))')

    def test_operator2(self):
        self.testParser = Parser()
        with self.assertRaises(MissedOperatorError):
            self.testParser.parseString('(22)')

    def test_operator3(self):
        self.testParser = Parser()
        with self.assertRaises(MissedOperatorError):
            self.testParser.parseString('(8)(3)')

    '''Checking if the parseString method actually evaluates to the right number.'''
    def test_valid1(self):
        self.testParser = Parser()
        self.assertEqual(self.testParser.parseString('(4*5)'), 20)

    def test_valid2(self):
        self.testParser = Parser()
        self.assertEqual(self.testParser.parseString('((2*3)*5)'), 30)

    def test_valid3(self):
        self.testParser = Parser()
        self.assertEqual(self.testParser.parseString('((2*4)*(5*6)) '), 240)

    '''Testing the Expression class. '''
    def test_expression1(self):
      newExpression = Expression(2, '*', 4)
      self.assertEqual(newExpression.evaluate(), 8)

    def test_expression2(self):
      nestedExpression = Expression(9, '+', 3)
      newExpression = Expression(nestedExpression, '*', 4)
      self.assertEqual(newExpression.evaluate(), 48)

    def test_expression3(self):
      with self.assertRaises(ZeroDivisionError):
        newExpression = Expression(9, '/', 0)
    
    


if __name__ == "__main__":
    p = Parser()
    test_check = str(input('Do you want to run the tests? Y/N: '))
    if test_check == 'Y':
        unittest.main()
    else:
        expression = str(input('Please enter an expression. '))
        evaluation = p.parseString(expression, True)
        if p.validateString() is True:
            tree = p.displayTree()
            print(
                f'The expression tree for the string {p.originalstring} is: ')
            print('\n')
            for x in tree:
                print(x)
            print('\n')
            print(
                f'The result for the expression {p.originalstring} is {evaluation}')
            ask = str(input('Would you like to save the tree into a file? Y/N: '))
            if ask == 'Y':
                p.pickleTree(tree)
            elif ask == 'N':
                loading = str(
                    input('Do you want to enter a filename for a tree to be loaded? Y/N: '))
                if loading == 'Y':
                    savedtree = p.loadTree()
                    for node in savedtree:
                        print(node)
                elif loading == 'N':
                    print('Program closed.')
                else:
                    raise MiscError('Invalid answer.')
            else:
                raise MiscError('Invalid answer.')
        else:
            raise MiscError('String not valid.')


