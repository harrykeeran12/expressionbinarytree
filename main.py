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

    
    

e = Expression(6, '/', 2)
f = Expression(e, '+', 5)

print(e.evaluate())
print(e.is_valid())
print(f.evaluate())
