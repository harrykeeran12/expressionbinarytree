'''All classes taken from the Data Structures and Algorithms in Python by Michael T Goodrich https://github.com/mjwestcott/Goodrich '''


class LinkedQueue:

    """FIFO queue implementation using a singly linked list for storage."""

    # -------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = '_element', '_next'         # streamline memory usage

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # ------------------------------- queue methods -------------------------------
    def __init__(self):
        """Create an empty queue."""
        self._head = None
        self._tail = None
        self._size = 0                          # number of queue elements

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def dequeue(self):
        """Remove and return the first element of the queue (i.e., FIFO).
        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Exception('Queue is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():                     # special case as queue is empty
            self._tail = None                     # removed head had been the tail
        return answer

    def enqueue(self, e):
        """Add an element to the back of queue."""
        newest = self._Node(e, None)            # node will be new tail node
        if self.is_empty():
            self._head = newest                   # special case: previously empty
        else:
            self._tail._next = newest
        self._tail = newest                     # update reference to tail node
        self._size += 1


class Tree:
    """Abstract base class representing a tree structure."""

    # ------------------------------- nested Position class -------------------------------
    class Position:
        """An abstraction representing the location of a single element within a tree.
        Note that two position instaces may represent the same inherent location in a tree.
        Therefore, users should always rely on syntax 'p == q' rather than 'p is q' when testing
        equivalence of positions.
        """

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not (self == other)            # opposite of __eq__

    # ---------- abstract methods that concrete subclass must support ----------
    def root(self):
        """Return Position representing the tree's root (or None if empty)."""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """Return Position representing p's parent (or None if p is root)."""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError('must be implemented by subclass')

    # ---------- concrete methods implemented in this class ----------
    def is_root(self, p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height2(self, p):                  # time is linear in size of subtree
        """Return the height of the subtree rooted at Position p."""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        """Return the height of the subtree rooted at Position p.
        If p is None, return the height of the entire tree.
        """
        if p is None:
            p = self.root()
        return self._height2(p)        # start _height2 recursion

    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.preorder()                            # return entire preorder iteration

    def preorder(self):
        """Generate a preorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):  # start recursion
                yield p

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p                                           # visit p before its subtrees
        for c in self.children(p):                        # for each child c
            # do preorder of c's subtree
            for other in self._subtree_preorder(c):
                yield other                                   # yielding each to our caller


class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure."""

    # --------------------- additional abstract methods ---------------------
    def left(self, p):
        """Return a Position representing p's left child.
        Return None if p does not have a left child.
        """
        raise NotImplementedError('must be implemented by subclass')

    def right(self, p):
        """Return a Position representing p's right child.
        Return None if p does not have a right child.
        """
        raise NotImplementedError('must be implemented by subclass')

    # ---------- concrete methods implemented in this class ----------
    def sibling(self, p):
        """Return a Position representing p's sibling (or None if no sibling)."""
        parent = self.parent(p)
        if parent is None:                    # p must be the root
            return None                         # root has no sibling
        else:
            if p == self.left(parent):
                return self.right(parent)         # possibly None
            else:
                return self.left(parent)          # possibly None

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.left(p) is not None:          # if left child exists, traverse its subtree
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p                               # visit p between its subtrees
        if self.right(p) is not None:         # if right child exists, traverse its subtree
            for other in self._subtree_inorder(self.right(p)):
                yield other

    # override inherited version to make inorder the default
    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.inorder()                 # make inorder the default


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    # -------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right'  # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    # -------------------------- nested Position class --------------------------
    class Position(BinaryTree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    # ------------------------------- utility methods -------------------------------
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:      # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    # -------------------------- binary tree constructor --------------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    # -------------------------- public accessors --------------------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:     # left child exists
            count += 1
        if node._right is not None:    # right child exists
            count += 1
        return count

    # -------------------------- nonpublic mutators --------------------------
    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.
        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2, respectively, as the left and right subtrees of the external Position p.
        As a side effect, set t1 and t2 to empty.
        Raise TypeError if trees t1 and t2 do not match type of this tree.
        Raise ValueError if Position p is invalid or not external.
        """
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):    # all 3 trees must be same type
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():         # attached t1 as left subtree of node
            t1._root._parent = node
            node._left = t1._root
            t1._root = None             # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():         # attached t2 as right subtree of node
            t2._root._parent = node
            node._right = t2._root
            t2._root = None             # set t2 instance to empty
            t2._size = 0


class ExpressionTree(LinkedBinaryTree):
    """An arithmetic expression tree."""

    def __init__(self, token, left=None, right=None):
        """Create an expression tree.
        In a single parameter form, token should be a leaf value (e.g., '42'),
        and the expression tree will have that value at an isolated node.
        In a three-parameter version, token should be an operator,
        and left and right should be existing ExpressionTree instances
        that become the operands for the binary operator.
        """
        super().__init__()                        # LinkedBinaryTree initialization
        if not isinstance(token, str):
            raise TypeError('Token must be a string')
        # use inherited, nonpublic method
        self._add_root(token)
        if left is not None:                      # presumably three-parameter form
            if token not in '+-*x/':
                raise ValueError('token must be valid operator')
            # use inherited, nonpublic method
            self._attach(self.root(), left, right)

    def __str__(self):
        """Return string representation of the expression."""
        pieces = []                 # sequence of piecewise strings to compose
        self._parenthesize_recur(self.root(), pieces)
        return ''.join(pieces)

    def _parenthesize_recur(self, p, result):
        """Append piecewise representation of p's subtree to resulting list."""
        if self.is_leaf(p):
            # leaf value as a string
            result.append(str(p.element()))
        else:
            # opening parenthesis
            result.append('(')
            self._parenthesize_recur(self.left(p), result)     # left subtree
            result.append(p.element())                         # operator
            self._parenthesize_recur(self.right(p), result)    # right subtree
            # closing parenthesis
            result.append(')')

    def evaluate(self):
        """Return the numeric result of the expression."""
        return self._evaluate_recur(self.root())

    def _evaluate_recur(self, p):
        """Return the numeric result of subtree rooted at p."""
        if self.is_leaf(p):
            return float(p.element())      # we assume element is numeric
        else:
            op = p.element()
            left_val = self._evaluate_recur(self.left(p))
            right_val = self._evaluate_recur(self.right(p))
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '/':
                return left_val / right_val
            else:                          # treat 'x' or '*' as multiplication
                return left_val * right_val


def tokenize(raw):
    """Produces list of tokens indicated by a raw expression string.
    For example the string '(43-(3*10))' results in the list
    ['(', '43', '-', '(', '3', '*', '10', ')', ')']
    """
    SYMBOLS = set('+-x*/() ')    # allow for '*' or 'x' for multiplication

    mark = 0
    tokens = []
    n = len(raw)
    for j in range(n):
        if raw[j] in SYMBOLS:
            if mark != j:
                tokens.append(raw[mark:j])  # complete preceding token
            if raw[j] != ' ':
                tokens.append(raw[j])       # include this token
            mark = j+1                    # update mark to being at next index
    if mark != n:
        tokens.append(raw[mark:n])      # complete preceding token
    return tokens


def build_expression_tree(tokens):
    """Returns an ExpressionTree based upon by a tokenized expression.
    tokens must be an iterable of strings representing a fully parenthesized
    binary expression, such as ['(', '43', '-', '(', '3', '*', '10', ')', ')']
    """
    S = []                                        # we use Python list as stack
    for t in tokens:
        if t in '+-x*/':                            # t is an operator symbol
            # push the operator symbol
            S.append(t)
        elif t not in '()':                         # consider t to be a literal
            # push trivial tree storing value
            S.append(ExpressionTree(t))
        elif t == ')':       # compose a new tree from three constituent parts
            right = S.pop()                           # right subtree as per LIFO
            op = S.pop()                              # operator symbol
            left = S.pop()                            # left subtree
            S.append(ExpressionTree(op, left, right))  # repush tree
        # we ignore a left parenthesis
    return S.pop()


if __name__ == '__main__':
    big = build_expression_tree(tokenize('((2+2)+(3*5))'))
    print(big, '=', big.evaluate())
    for i in big.positions():
        print(big.depth(i) * ' ' + str(i.element()))
