import operator as op
class Expression:
  'An Expression class, which takes in either an integer between 0-9 as the operands, or another instance of the expression class, as well as the operator.'
  def __init__(self, operand1, operator, operand2):
    if type(operand1) == Expression:
      self.X = operand1.evaluate()
    else:
      self.X = operand1
    if type(operand2) == Expression:
      self.Y = operand2.evaluate()
    else:
      self.Y = operand2
    if operator == '+':
      self.operator = op.add
    elif operator == '-':
      self.operator = op.sub
    elif operator == '/':
      self.operator = op.truediv
      #remember to validate divisions.
    elif operator == '*':
      self.operator = op.mul

    self.type = (type(operand1), type(operand2))
  def is_valid(self):
    'Checks if the expression is valid.'
    if (type(self.operator(self.X, self.Y)) is int) or (type(self.operator(self.X, self.Y)) is float):
      return True
    else: 
      return False
  def evaluate(self):
    'Evaluates the operation in the instance.'
    try:
      return self.operator(self.X, self.Y)
    except:
      print('Error')

    
    
#destructuring the expression (((2 x (3+2)) + 5)/2)
e1 = Expression(3,'+',2)
e2 = Expression(2, '*', e1)
e3 = Expression(e2, '+', 5)
e4 = Expression(e3, '/', 2)


""" print(e.evaluate())
print(f.evaluate())
print(g.evaluate()) """

class Parser:
  def __init__(self, input):
    self.input = input.replace(" ", "")#removes whitespace from string.
    self.bracketStack = ArrayStack()
    self.operatorStack = ArrayStack()
  def parse(self):
    'Parses an expression written as a string.'
    operators = ['+', '-', '*', '/']
    for x in range(len(self.input)):
      if self.input[x] == '(':
        self.bracketStack.push(self.input[x])
      elif self.input[x] == ')':
        self.bracketStack.push(self.input[x])
        #handle )( somehow.


      if self.input[x] in operators:
        self.operatorStack.push(self.input[x])
    print(self.operatorStack.data)

    if len(self.bracketStack) % 2 != 0:
      raise Exception('Not a valid expression, brackets mismatched.')
    if len(self.operatorStack) < len(self.bracketStack) / 2:
      raise Exception('Not a valid expression, operator missing.')
    if len(self.operatorStack) != len(self.bracketStack) / 2:
      raise Exception('Not a valid expression, wrong number of operands.')
  def replaceString(self, input):
    self.input = input.replace(" ", "")#removes whitespace from string.
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
    self.data.append(e) # new item stored at end of list
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
    return self.data.pop( ) # remove last item from list


p = Parser('(((2 * (3+2)) + 5)/2)')
#p.replaceString('(2*4)*(3+2)')
p.parse()
