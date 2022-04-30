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
    return self.data.pop() # remove last item from list
  def empty(self):
    '''Clears the stack.'''
    self.data = []
class Parser:
  def __init__(self):
    self.input = ''
    self.expressions = ArrayStack()
  def parseString(self, input):
    'Parses an expression written as a string.'
    self.expressions.empty()
    self.input = input.replace(" ", "")#removes whitespace from string.
    self.bracketStack = ArrayStack()
    self.operatorStack = ArrayStack()
    operators = ['+', '-', '*', '/']
    for x in range(len(self.input)):
      if self.input[x] == '(':
        self.bracketStack.push(x)
      elif self.input[x] == ')':
        self.bracketStack.push(x)
      if self.input[x] in operators:
        self.operatorStack.push(x)#get the indexes of the operators.

    #print(self.operatorStack.data)
    
    if self.validateString() == True:
      #Parsing of the expression.
      for i in self.bracketStack.data:
        for j in self.bracketStack.data:
          if i != j and abs(i-j) > 2 and i < j:
            valid = self.input[i:j+1]
            if '(' in valid and ')' in valid:
              operatorloc = [x for x in range(len(valid)) if valid[x] in ['+', '-', '*', '/']] 
              op1 = valid[1:operatorloc[0]]
              op2 = valid[operatorloc[0]+1: -1]
              if abs(i-j) >= 4 and len(operatorloc) == 1 and (op1.isdigit() == True and op2.isdigit() == True):
                  print('Shortest expression = ', valid)
                  shortest = valid
                  e = Expression(int(op1), valid[operatorloc[0]], int(op2))
                  output = e.evaluate()
                  if len(self.bracketStack) > 2:
                    return self.parseString(self.input.replace(shortest, str(output)))
                  self.expressions.push(e)
                  return output
            else:
                pass

  def validateString(self):
    '''Validates the string.'''
    if len(self.bracketStack) % 2 != 0:
      raise Exception('Not a valid expression, brackets mismatched.')
    elif len(self.operatorStack) < len(self.bracketStack) / 2:
      raise Exception('Not a valid expression, operator missing.')
    elif len(self.operatorStack) != len(self.bracketStack) / 2:
      raise Exception('Not a valid expression, wrong number of operands.')
    else: 
      return True


if __name__ == "__main__":
  p = Parser()
  print(p.parseString('((2+2)*3)'))
  print(p.parseString('((2*4)*(3+2))'))
  print(p.parseString('(((2 * (3+2)) + 5)/2)'))

