from sqlListener import sqlListener
from dbFileManager import dbFileManager
from dataManager import dbDataManager
import pdb

if __name__ is not None and "." in __name__:
    from .sqlParser import sqlParser
else:
    from sqlParser import sqlParser

fileManager = dbFileManager()
dataManager = dbDataManager()


class tokenInterpreter(sqlListener):
    def __init__(self):
        pass

    def exitR(self, ctx):
        print("Hello world. At the input has been already validated")

    def getTokenValue(self, name):
        return name.getText()

    # CREATE DATABASE SECTION
    def enterCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        database_name = self.getTokenValue(ctx.database_name())
        fileManager.createDatabaseFS(database_name)

    def exitCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        print("DATABASE CREATE EXECUTED")
        pass

    # !CREATE DATABASE SECTION
    # SHOW DATABASE SECTION
    def enterShow_databases_stmt(self, ctx: sqlParser.Show_databases_stmtContext):
        print("bases de datos en sistema:")
        print(fileManager.showDatabasesFS())
        pass

    # !SHOW DATABASE SECTION
    # USE DATABASE SECION
    def enterUse_database_stmt(self, ctx: sqlParser.Use_database_stmtContext):
        datbase_name = self.getTokenValue(ctx.database_name())
        fileManager.useDatabaseFS(datbase_name)
        print("current database changed to: " + datbase_name)

    # !USE DATABASE SECION
    # DROP DATABASE SECTION
    def enterDrop_database_stmt(self, ctx: sqlParser.Drop_database_stmtContext):
        database_name = self.getTokenValue(ctx.database_name())
        fileManager.removeDatabaseFS(database_name)
        pass

    # !DROP DATABASE SECTION
    # CREATE TABLE SECTION
    def enterCreate_table_stmt(self, ctx: sqlParser.Create_table_stmtContext):
        table_name = self.getTokenValue(ctx.table_name())
        cols = []
        for column in ctx.column_def():
            type = dataManager.validateCreateTableTypes(self.getTokenValue(column.type_name().name()[0]))
            key = self.getTokenValue(column.column_name())
            cols.append((key, type))
        # create database files
        if fileManager.createTableFS(table_name, cols):
            print("SE HA CREADO LA TABLA " + table_name + " EXITOSAMENTE")
        pass

    # !CREATE TABLE SECTION
    # SHOW TABLES SECTION
    def enterShow_tables_stmt(self, ctx: sqlParser.Show_tables_stmtContext):
        print("TABLES IN " + fileManager.getDatabaseFS())
        print(fileManager.showTablesFS())
        pass

    # SHOW TABLES SECTION
    # INSERT SECTION
    def enterInsert_stmt(self, ctx: sqlParser.Insert_stmtContext):

        tableName = self.getTokenValue(ctx.table_name())
        tableData = eval(fileManager.readTableFS(tableName, "data"))

        # table structure
        tableStructure = eval(fileManager.readTableFS(tableName, "structure"))
        # input col structure
        targetCols = [self.getTokenValue(col) for col in ctx.column_name()]

        newData = []

        values = [self.getTokenValue(value) for value in ctx.expr()]
        colNames = [col[0] for col in tableStructure]
        colTypes = [col[1] for col in tableStructure]

        if len(values) > len(tableStructure):
            raise ValueError("INSERT REQUEST HAS MORE VALUES THAN THE TABLE LENGTH")

        # specific insert stmt
        if len(targetCols):
            newData = [""] * len(tableStructure)
            for targetCol in targetCols:
                if targetCol in colNames:
                    colIndex = targetCols.index(targetCol)
                else:
                    raise ValueError("COLUMN " + targetCol + " DOES NOT EXIST IN TABLE " + tableName)
                newData[colIndex] = dataManager.matchData(colTypes[colIndex], values[colIndex])



        # regular insert stmt
        else:
            index = 0
            for value in ctx.expr():
                newData.append(dataManager.matchData(tableStructure[index][1], self.getTokenValue(value)))
                index = index + 1

        if len(newData):
            if None in newData:
                raise ValueError("INSERT QUERY HAS UNCONSISTENT TYPES")
            tableData.append(tuple(newData))
            fileManager.insertTableFS(tableName, str(tableData))
            print("INSERT A " + tableName + " EXITOSO")
        else:
            dataManager.raiseError(False, "CANNOT INSERT EMPTY TUPLE")

    # !INSERT SECTION
    # SELECT SECTION
    def enterSelect_core(self, ctx: sqlParser.Select_coreContext):

        tableName = self.getTokenValue(ctx.table_or_subquery()[0].table_name())

        tableStructure = eval(fileManager.readTableFS(tableName, "structure"))
        tableData = eval(fileManager.readTableFS(tableName, "data"))
        colNames = [col[0] for col in tableStructure]

        # check if table exists in database
        if tableName not in fileManager.showTablesFS():
            raise ValueError("TABLE " + tableName + " DOES NOT EXIST IN " + fileManager.currentDatabase)

        dataManager.setSavedData(tableData)
        dataManager.setSavedStructure(tableStructure)

        # insert target columns
        targets = [self.getTokenValue(target) for target in ctx.result_column()]

        if "*" in targets:
            # @TODO: STUFF TO SELECT * COLS, INCLUDING REDUCE
            print("send data to Manager")
        else:
            if all(elem in targets for elem in colNames):
                print("send data to Manager")
            else:
                raise ValueError("ATLEAST ONE OF THE TARGET TABLES DOES NOT EXIST IN " + tableName)

    # !SELECT SECTION

    # SELECT REDUCE (WHERE) SECTION
    def enterExprComparisonSecond(self, ctx: sqlParser.ExprComparisonSecondContext):
        targetTable = self.getTokenValue(ctx.expr()[0])
        targetCostraint = self.getTokenValue(ctx.expr()[1])
        targetCondition = self.getTokenValue(ctx.children[1])

        print("accept data and reduce")

    # SELECT REDUCE (WHERE) SECTION
