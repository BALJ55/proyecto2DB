import pdb
from datetime import date
import re
from collections import OrderedDict
from dataRegex import dataValidator

dv = dataValidator().getValidationRegex()


class dbDataManager():
    allowedDataTypes = ['INT', 'FLOAT', 'DATE', 'CHAR']
    savedData = []
    cachedData = []
    savedStructure = []
    multiples = False
    reductor = ""

    def __init__(self):
        pass

    def validateCreateTableTypes(self, input):
        if input not in self.allowedDataTypes:
            raise ValueError(input + " IS NOT A VALID DATA TYPE")
        else:
            return input

    def queryWhereStringCLBuilder(self, index, reducer, condition):

        index = str(index)
        if condition == '<':
            return str("item[" + index + "] < " + reducer)
        if condition == '<=':
            return str("item[" + index + "] <= " + reducer)
        if condition == '>':
            return str("item[" + index + "] > " + reducer)
        if condition == '>=':
            return str("item[" + index + "] >= " + reducer)
        if condition == '<>':
            return str("item[" + index + "] != " + reducer)
        if condition == '=':
            return str("item[" + index + "] == " + reducer)

    def queryWhereAgregatorBuilder(self, array, operator, comparator):
        if operator == 'AND':
            return (tup for tup in array if operator)

    def matchData(self, type, value):
        if type == "INT":
            try:
                return int(value)
            except Exception:
                print(value + " IS NOT A INTEGER")
        if type == "FLOAT":
            try:
                return float(value)
            except Exception:
                print(value + " IS NOT A FLOAT")
        if type == "CHAR" or type == "DATE" or type == "VARCHAR":
            try:
                return str(value)
            except Exception:
                print(value + " IS NOT A CHAR OR DATE")

    def generateSpecificColOrder(self, cols, structure):
        return [any(e[0] == col for e in structure) for col in cols]

    def raiseError(self, condition, message):
        if condition:
            pass
        else:
            raise ValueError(message)

    def setSavedData(self, data):
        self.savedData = data

    def setSavedStructure(self, structure):
        self.savedStructure = structure

    def setCachedData(self, data):
        self.cachedData = data

    def addToCache(self, data):
        self.cachedData.append(data)

    def handleNullValue(self, data, bc):
        returnData = []
        for item in data:
            try:
                if eval(bc):
                    returnData.append(item)
            except TypeError:
                pass
        return returnData

    def handleAndStmt(self,listas):
        return [element for element in listas[0] if element in listas[1]]

    def handleOrStmt(self,listas):
        return listas[1] + [x for x in listas[0] if x not in listas[1]]