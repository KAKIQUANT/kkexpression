import numpy as np

from factor.alpha import AlphaLit

# from expr import *
#
# from dataloader import *

class BinaryCombinedFactor:

    def __init__(self, left, right, operator):

        if not (isinstance(left, Factor) or isinstance(left, BinaryCombinedFactor)) and (operator == 'add' or operator == 'multiply' or operator == 'and' or operator == 'or'):
            exchange = left
            left = right
            right = exchange
        if isinstance(left, BinaryCombinedFactor) and not isinstance(left, Factor):
            self.LeftField = left.field
            self.LeftExpr = left.expr
        else:
            if isinstance(left, Factor):
                self.LeftField = "Factor('" + left.name + "')"
            else:
                self.LeftField = str(left)
            self.LeftExpr = left

        if isinstance(right, BinaryCombinedFactor) and not isinstance(left, Factor):
            self.RightField = right.field
            self.RightExpr = right.expr
        else:
            if isinstance(right, Factor):
                self.RightField = "Factor('" + right.name + "')"
                self.RightExpr = right
            else:
                self.RightField = str(right)
                self.RightExpr = float(right)


        if operator == 'add':
            self.operator = np.add

        if operator == 'subtract':
            self.operator = np.subtract

        if operator == 'multiply':
            self.operator = np.multiply

        if operator == 'divide':
            self.operator = np.divide

        if operator == 'power':
            self.operator = np.power

        if operator == 'mod':
            self.operator = np.mod

        if operator == 'floordiv':
            self.operator = np.floor_divide

        if operator == 'and':
            self.operator = np.logical_and

        if operator == 'or':
            self.operator = np.logical_or

        if operator == 'not':
            self.operator = np.logical_not

        if operator == 'ne':
            self.operator = np.not_equal

        if operator == 'gt':
            self.operator = np.greater

        if operator == 'lt':
            self.operator = np.less

        if operator == 'le':
            self.operator = np.less_equal

        if operator == 'ge':
            self.operator = np.greater_equal



        if right == None:
            self.field = operator + '(' + self.LeftField + ')'
            self.expr = (self.operator, (self.LeftExpr,))
        else:
            self.field = operator + '(' + self.LeftField + ', ' + self.RightField + ')'
            self.expr = (self.operator, (self.LeftExpr, self.RightExpr))

    def __add__(self, other):
        return BinaryCombinedFactor(self, other, 'add')

    def __radd__(self, other):
        return BinaryCombinedFactor(other, self, 'add')

    def __sub__(self, other):
        return BinaryCombinedFactor(self, other, 'subtract')

    def __rsub__(self, other):
        return BinaryCombinedFactor(other, self, 'subtract')

    def __mul__(self, other):
        return BinaryCombinedFactor(self, other, 'multiply')

    def __rmul__(self, other):
        return BinaryCombinedFactor(other, self, 'multiply')

    def __truediv__(self, other):
        return BinaryCombinedFactor(self, other, 'divide')

    def __rtruediv__(self, other):
        return BinaryCombinedFactor(other, self, 'divide')

    def __pow__(self, other):
        return BinaryCombinedFactor(self, other, 'power')

    def __rpow__(self, other):
        return BinaryCombinedFactor(other, self, 'power')

    def __mod__(self, other):
        return BinaryCombinedFactor(self, other, 'mod')

    def __rmod__(self, other):
        return BinaryCombinedFactor(other, self, 'mod')

    def __floordiv__(self, other):
        return BinaryCombinedFactor(self, other, 'floordiv')

    def __rfloordiv__(self, other):
        return BinaryCombinedFactor(other, self, 'floordiv')

    def __and__(self, other):
        return BinaryCombinedFactor(self, other, 'and')

    def __rand__(self, other):
        return BinaryCombinedFactor(other, self, 'and')

    def __or__(self, other):
        return BinaryCombinedFactor(self, other, 'or')

    def __ror__(self, other):
        return BinaryCombinedFactor(other, self, 'or')

    def __invert__(self):
        return BinaryCombinedFactor(self, None, 'not')

    def __ne__(self, other):
        return BinaryCombinedFactor(self, other, 'ne')

    def __gt__(self, other):
        return BinaryCombinedFactor(self, other, 'gt')

    def __lt__(self, other):
        return BinaryCombinedFactor(self, other, 'lt')

    def __le__(self, other):
        return BinaryCombinedFactor(self, other, 'le')

    def __ge__(self, other):
        return BinaryCombinedFactor(self, other, 'ge')


    def __repr__(self):
        return self.field


class Factor(BinaryCombinedFactor):

    def __init__(self, name):
        fields, names = AlphaLit.get_fields_names(1)
        self.name = name
        for f, n in zip(fields, names):
            if n == name:
                self.field = f
                break


    def __repr__(self):
        return "Factor('" + self.name + "')"


def execute_factor(factor, order_book_ids, start_date, end_date):
    if isinstance(factor, Factor):
        #return CSVDataloader(config.data_path, order_book_ids, start_date, end_date).load_data([factor.field], [factor.name])[factor.name]
        return 1

    if not isinstance(factor, Factor) and not isinstance(factor, BinaryCombinedFactor):
        return factor

    return factor.expr[0](execute_factor(factor.expr[1][0], order_book_ids, start_date, end_date), execute_factor(factor.expr[1][1], order_book_ids, start_date, end_date))

print(3+Factor('rank_roc_5_rank_roc_10')+2)
print((3+Factor('rank_roc_5_rank_roc_10')+2).expr)
