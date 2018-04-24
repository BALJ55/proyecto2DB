import pdb
from datetime import date

class dbDataManager():
    allowedDataTypes = ['INT', 'FLOAT', 'DATE', 'CHAR']

    def __init__(self):
        pass

    def validateCreateTableTypes(self, input):
        if input not in self.allowedDataTypes:
            raise ValueError(input + "NO ES UN TIPO DE DATO VALIDO")
        else:
            return True

    def queryWhereConditionBuilder(self, key, array, filter, comparator):
        if key == '<':
            return array[filter] < comparator
        if key == '<=':
            return array[filter] <= comparator
        if key == '>':
            return array[filter] > comparator
        if key == '>=':
            return array[filter] >= comparator
        if key == '<>':
            return array[filter] != comparator
        if key == '=':
            return array[filter] == comparator

    def queryWhereAgregatorBuilder(self, array, operator, comparator):
        if operator == 'AND':
            return (tup for tup in array if operator)

    def queryWhereResultBuilder(self, array, filters):

        print((filter for filter in filters))
        # return (tup for tup in array if (filter for filter in filters))

    def obtainValueFromColumn(self,col):
        if hasattr(col, 'column_name'):
            return col.column_name()
        if hasattr(col, 'literal_value'):
            return col.literal_value()

    def getDataInFormat(self,param):
        try:
            return int(param)
        except Exception:
            pass
        try:
            return float(param)
        except Exception:
            pass
        return param

