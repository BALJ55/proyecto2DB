from sqlListener import sqlListener
from dbFileManager import dbFileManager
from dataManager import dbDataManager
from dataPrinter import dbDataPrinter
import pdb

if __name__ is not None and "." in __name__:
    from .sqlParser import sqlParser
else:
    from sqlParser import sqlParser

fileManager = dbFileManager()
dataManager = dbDataManager()
dataPrinter = dbDataPrinter()


class tokenInterpreter(sqlListener):
    def __init__(self, verbose, displayRegex):
        if displayRegex:
            print("using the following regex to filter data:")
            print(dataManager.dv)
        self.verbouseOutput = verbose
        pass

    def exitR(self, ctx):
        print("Hello world. At the input has been already validated")

    def getTokenValue(self, name):
        return name.getText()

    # CREATE DATABASE SECTION
    def enterCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        dataManager.verboseOutput(self.verbouseOutput, "CATCHING DATABASE NAME FROM LEXER")
        database_name = self.getTokenValue(ctx.database_name())
        dataManager.verboseOutput(self.verbouseOutput, "CREATING DATABASE FILES")
        fileManager.createDatabaseFS(database_name)
        dataManager.verboseOutput(self.verbouseOutput, "DATABASE FILES CREATED")

    def exitCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        print("DATABASE CREATE EXECUTED")
        pass

    # !CREATE DATABASE SECTION
    # SHOW DATABASE SECTION
    def enterShow_databases_stmt(self, ctx: sqlParser.Show_databases_stmtContext):
        print("DATABASES IN SYSTEM:")
        dataPrinter.print_table(
            [[table] for table in fileManager.showDatabasesFS()],
            ['DATABASES'])
        pass

    # !SHOW DATABASE SECTION
    # USE DATABASE SECION
    def enterUse_database_stmt(self, ctx: sqlParser.Use_database_stmtContext):
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING DATABASE NAME FROM LEXER")
        datbase_name = self.getTokenValue(ctx.database_name())
        dataManager.verboseOutput(self.verbouseOutput, "SETTING CURRENT DATABASE TO " + datbase_name)
        fileManager.useDatabaseFS(datbase_name)
        print("current database changed to: " + datbase_name)

    # !USE DATABASE SECION
    # DROP DATABASE SECTION
    def enterDrop_database_stmt(self, ctx: sqlParser.Drop_database_stmtContext):
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING DATABASE NAME FROM LEXER")
        database_name = self.getTokenValue(ctx.database_name())
        dataManager.verboseOutput(self.verbouseOutput, "REMOVING DATABASE NAME FROM LEXER")
        fileManager.removeDatabaseFS(database_name)
        pass

    # !DROP DATABASE SECTION
    # CREATE TABLE SECTION
    def enterCreate_table_stmt(self, ctx: sqlParser.Create_table_stmtContext):
        table_name = self.getTokenValue(ctx.table_name())
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE NAME FROM LEXER")

        cols = []
        dataManager.verboseOutput(self.verbouseOutput, "GENERATING TABLE STRUCTURE FROM TOKENS")

        for column in ctx.column_def():
            type = dataManager.validateCreateTableTypes(self.getTokenValue(column.type_name().name()[0]))
            key = self.getTokenValue(column.column_name())
            cols.append((key, type))
        # create database files
        dataManager.verboseOutput(self.verbouseOutput, "ATTEMPTING TO CREATE DATABASE FILES")

        if fileManager.createTableFS(table_name, cols):
            print("TABLE " + table_name + " CREATED SUCCESSFULLY")
        pass

    # !CREATE TABLE SECTION
    def enterDrop_table_stmt(self, ctx: sqlParser.Drop_table_stmtContext):
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE NAME FROM LEXER")
        table_name = self.getTokenValue(ctx.table_name())
        dataManager.verboseOutput(self.verbouseOutput, "REMOVING TABLE NAME FROM LEXER")
        fileManager.removeTableFS(table_name)
        pass

    # SHOW TABLES SECTION
    def enterShow_tables_stmt(self, ctx: sqlParser.Show_tables_stmtContext):
        print("TABLES IN " + fileManager.getDatabaseFS())
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING DATABASES FROM FILE SYSTEM")

        dataPrinter.print_table(
            [[table] for table in fileManager.showTablesFS()],
            ['TABLES'])
        pass

    # SHOW TABLES SECTION
    # SHOW COLUMNS IN SECTION WITH DESCRIPTION
    def enterShow_columns_stmt(self, ctx: sqlParser.Show_columns_stmtContext):
        tableName = self.getTokenValue(ctx.table_name())
        dataPrinter.print_table([table for table in eval(fileManager.showColumnsFS(tableName, "structure"))],['Column Name', "type"])


    # INSERT SECTION
    def enterInsert_stmt(self, ctx: sqlParser.Insert_stmtContext):

        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE NAME FROM LEXER")
        tableName = self.getTokenValue(ctx.table_name())

        dataManager.verboseOutput(self.verbouseOutput, "FETCHING SAVED TABLE DATA FROM FILE SYSTEM")
        tableData = eval(fileManager.readTableFS(tableName, "data"))

        # table structure
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING SAVED TABLE STRUCTURE FROM FILE SYSTEM")
        tableStructure = eval(fileManager.readTableFS(tableName, "structure"))

        # input col structure
        dataManager.verboseOutput(self.verbouseOutput, "GENERATING TARGET COLUMNS FROM LEXER")
        targetCols = [self.getTokenValue(col) for col in ctx.column_name()]

        newData = []

        dataManager.verboseOutput(self.verbouseOutput, "GENERATING INSERT VALUES FROM LEXER")
        values = [self.getTokenValue(value) for value in ctx.expr()]
        colNames = [col[0] for col in tableStructure]
        colTypes = [col[1] for col in tableStructure]

        dataManager.verboseOutput(self.verbouseOutput, "EVALUATING DATA LENGTH")
        if len(values) > len(tableStructure):
            raise ValueError("INSERT REQUEST HAS MORE VALUES THAN THE TABLE LENGTH")

        # specific insert stmt
        dataManager.verboseOutput(self.verbouseOutput, "EVALUATING IF SPECIFIC COLUMNS WERE DECLARED")

        if len(targetCols):
            dataManager.verboseOutput(self.verbouseOutput, "SPECIFIC COLUMNS WERE DECLARED")

            newData = [""] * len(tableStructure)
            for targetCol in targetCols:
                dataManager.verboseOutput(self.verbouseOutput, "VALIDATING COLUMN NAME")
                if targetCol in colNames:
                    colIndex = targetCols.index(targetCol)
                    valueIndex = colNames.index(targetCol)
                    if not len(values) > valueIndex:
                        dataManager.verboseOutput(self.verbouseOutput, "COLUMN VALUE WAS NOT DEFINED, SETTING TO NULL")
                        newData[colIndex] = 'NULL'
                    else:
                        dataManager.verboseOutput(self.verbouseOutput, "COLUMN VALUE WAS DEFINED")
                        newData[colIndex] = dataManager.matchData(colTypes[colIndex], values[valueIndex])
                else:
                    dataManager.verboseOutput(self.verbouseOutput,
                                              "INVALID COLUMN NAME, DOES NOT EXIST IN TABLE DEFINITION")
                    raise ValueError("COLUMN " + targetCol + " DOES NOT EXIST IN TABLE " + tableName)

        # regular insert stmt
        else:
            dataManager.verboseOutput(self.verbouseOutput, "SPECIFIC COLUMNS WERE NOT DECLARED")
            index = 0
            dataManager.verboseOutput(self.verbouseOutput, "VALIDATING NEW DATA WITH TABLE STRUCTURE DEFINITION")
            for value in ctx.expr():
                newData.append(dataManager.matchData(tableStructure[index][1], self.getTokenValue(value)))
                index = index + 1

        dataManager.verboseOutput(self.verbouseOutput, "VALIDATING NON NULL INPUT")
        if len(newData):
            if None in newData:
                raise ValueError("INSERT QUERY HAS UNCONSISTENT TYPES")
            dataManager.verboseOutput(self.verbouseOutput, "DATA INPUT SUCCESSFULL")
            tableData.append(tuple(newData))
            fileManager.insertTableFS(tableName, str(tableData))
            print("INSERT TO " + tableName + " SUCCESSFULL")
        else:
            dataManager.raiseError(False, "CANNOT INSERT EMPTY TUPLE")

    # !INSERT SECTION
    # SELECT SECTION
    def enterSelect_core(self, ctx: sqlParser.Select_coreContext):
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE NAME FROM LEXER")
        tableName = self.getTokenValue(ctx.table_or_subquery()[0].table_name())

        # check if table exists in database
        dataManager.verboseOutput(self.verbouseOutput, "CHECKING IF TABLE EXISTS IN CURRENT DATABASE")
        if tableName not in fileManager.showTablesFS():
            raise ValueError("TABLE " + tableName + " DOES NOT EXIST IN " + fileManager.currentDatabase)

        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE STRUCTURE FROM FILE SYSTEM")
        tableStructure = eval(fileManager.readTableFS(tableName, "structure"))

        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE DATA FROM FILE SYSTEM")
        tableData = eval(fileManager.readTableFS(tableName, "data"))
        colNames = [col[0] for col in tableStructure]

        dataManager.verboseOutput(self.verbouseOutput,
                                  "SETTING TABLE STRUCTURE IN DATA MANAGER FOR REDUCTION OPERATIONS")

        # insert target columns
        targets = [self.getTokenValue(target) for target in ctx.result_column()]

        dataManager.verboseOutput(self.verbouseOutput, "CHECKING IF QUERY IS SELECT *")
        dataManager.setSavedStructure(tableStructure)

        if "*" in targets:
            dataManager.verboseOutput(self.verbouseOutput, "QUERY IS SELECT *")
            dataManager.setSavedData(tableData)
        else:
            dataManager.verboseOutput(self.verbouseOutput, "QUERY HAS SPECIFIC COLUMNS DECLARED")
            dataManager.verboseOutput(self.verbouseOutput, "VALIDATING TARGET COLUMNS WITH SAVED STRUCTURE")
            if all(value in colNames for value in targets):
                targetsIndex = [colNames.index(elem) for elem in targets]
                dataManager.selectStruct(targetsIndex)
                dataManager.verboseOutput(self.verbouseOutput, "DATA SAVED IN DATA MANAGER")
                dataManager.setSavedData(tableData)
            else:
                dataManager.verboseOutput(self.verbouseOutput, "FOUND INCONSISTENT DECLARATION IN QUERY")
                raise ValueError("ATLEAST ONE OF THE TARGET TABLES DOES NOT EXIST IN " + tableName)

        # Exit a parse tree produced by sqlParser#select_core.

    def exitFactored_select_stmt(self, ctx: sqlParser.Factored_select_stmtContext):
        dataManager.verboseOutput(self.verbouseOutput, "PRINTING SAVED DATA FROM FILE MANAGER")
        structure = [col[0] for col in dataManager.savedStructure]
        finalData = dataManager.savedData

        if len(dataManager.specificColsArray):

            filteredData = []
            newStructure = []
            dataManager.verboseOutput(self.verbouseOutput, "FILTERING DATA")
            for tup in finalData:
                filteredValue = []
                for col in dataManager.specificColsArray:
                    filteredValue.append(tup[col])
                filteredData.append(tuple(filteredValue))
            finalData = filteredData
            for colIndex in range(0,len(structure)):
                if colIndex in dataManager.specificColsArray:
                    newStructure.append(structure[colIndex])
            structure = newStructure


        exprs = ctx.expr()
        if len(exprs):
            limit = self.getTokenValue(exprs[0])
            finalData = finalData[:int(limit)]

        dataPrinter.print_table(finalData, structure)
        # print(dataManager.savedData)

    # !SELECT SECTION

    # SELECT REDUCE (WHERE) SECTION
    def enterExprComparisonFirst(self, ctx: sqlParser.ExprComparisonSecondContext):
        dataManager.verboseOutput(self.verbouseOutput, "WHERE CLAUSE OPERATION")

        dataManager.verboseOutput(self.verbouseOutput, "CHECKING TREE FOR OTHER WHERE OPERATIONS")
        if dataManager.multiples:
            dataManager.verboseOutput(self.verbouseOutput, "AND/OR NODES WILL HANDLE REDUCTION, PASSING...")
            pass
        else:
            print("we in bois")
            dataManager.verboseOutput(self.verbouseOutput, "SIMPLE WHERE REDUCTION")
            dataManager.verboseOutput(self.verbouseOutput, "GENERATING REDUCTION FILTER")

            builtCondition = dataManager.queryWhereStringCLBuilder(
                [col[0] for col in dataManager.savedStructure].index(self.getTokenValue(ctx.expr()[0])),
                self.getTokenValue(ctx.expr()[1]),
                self.getTokenValue(ctx.children[1])
            )
            print(builtCondition)
            dataManager.verboseOutput(self.verbouseOutput, "SAVING REDUCED DATA")

            dataManager.setSavedData(dataManager.handleNullValue(dataManager.savedData, builtCondition))

    # ! SELECT REDUCE (WHERE) SECTION
    # ALTER TABLE SECTION
    def enterAlter_table_stmt(self, ctx: sqlParser.Alter_table_stmtContext):
        # se llama al show tables del FileManager
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE NAME FROM LEXER")
        table_name_old = self.getTokenValue(ctx.table_name())

        dataManager.verboseOutput(self.verbouseOutput, "FETCHING NEW TABLE NAME FROM LEXER")
        table_name_new = self.getTokenValue(ctx.new_table_name())
        r = fileManager.showTablesFS()
        check = False
        for tables in r:
            if (tables == table_name_old):
                check = True
        if (check):
            dataManager.verboseOutput(self.verbouseOutput, "RENAMING TABLE")
            (fileManager.renameFS(table_name_old, table_name_new))

    # ! ALTER TABLE SECTION
    # SELECT AND SECTION

    def enterExprAnd(self, ctx: sqlParser.ExprAndContext):
        dataManager.verboseOutput(self.verbouseOutput, "AND NODE DETECTED")

        dataManager.verboseOutput(self.verbouseOutput, "SETTING IGNORE STATE FOR SIMPLE WHERE CLAUSE")
        dataManager.multiples = True
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING CONDITIONS")
        conditions = ctx.expr()
        reducedData = []

        dataManager.verboseOutput(self.verbouseOutput, "BUILDING REDUCE STATEMENTS")
        for condition in conditions:
            builtCondition = dataManager.queryWhereStringCLBuilder(
                [col[0] for col in dataManager.savedStructure].index(self.getTokenValue(condition.expr()[0])),
                self.getTokenValue(condition.expr()[1]),
                self.getTokenValue(condition.children[1])
            )
            dataManager.verboseOutput(self.verbouseOutput, "FILTERING DATA")
            reducedData.append(dataManager.handleNullValue(dataManager.savedData, builtCondition))

        dataManager.verboseOutput(self.verbouseOutput, "SAVING DATA IN DATA MANAGER")
        dataManager.setSavedData(dataManager.handleAndStmt(reducedData))

    # ! SELECT AND SECTION
    # SELECT OR SECTION
    def enterExprOr(self, ctx: sqlParser.ExprOrContext):
        dataManager.verboseOutput(self.verbouseOutput, "OR NODE DETECTED")

        dataManager.verboseOutput(self.verbouseOutput, "SETTING IGNORE STATE FOR SIMPLE WHERE CLAUSE")
        dataManager.multiples = True

        dataManager.verboseOutput(self.verbouseOutput, "FETCHING CONDITIONS")
        conditions = ctx.expr()
        reducedData = []

        dataManager.verboseOutput(self.verbouseOutput, "BUILDING REDUCE STATEMENTS")
        for condition in conditions:
            builtCondition = dataManager.queryWhereStringCLBuilder(
                [col[0] for col in dataManager.savedStructure].index(self.getTokenValue(condition.expr()[0])),
                self.getTokenValue(condition.expr()[1]),
                self.getTokenValue(condition.children[1])
            )
            reducedData.append(dataManager.handleNullValue(dataManager.savedData, builtCondition))

        dataManager.verboseOutput(self.verbouseOutput, "SAVING DATA IN DATA MANAGER")
        dataManager.setSavedData(dataManager.handleOrStmt(reducedData))

    # ! SELECT OR SECTION
    # UPDATE SECTION
    def enterUpdate_stmt(self, ctx: sqlParser.Update_stmtContext):

        dataManager.verboseOutput(self.verbouseOutput, "UPDATE NODE DETECTED")
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING QUERY DATA FROM LEXER")

        targetTable = self.getTokenValue(ctx.table_name())
        targetCols = [self.getTokenValue(col) for col in ctx.column_name()]

        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE STRUCTURE FROM FILE SYSTEM")

        tableStructure = eval(fileManager.readTableFS(targetTable, "structure"))
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE DATA FROM FILE SYSTEM")

        tableData = eval(fileManager.readTableFS(targetTable, "data"))
        colNames = [col[0] for col in tableStructure]

        if targetTable not in fileManager.showTablesFS():
            raise ValueError("TABLE " + targetTable + " DOES NOT EXIST IN " + fileManager.currentDatabase)
        if all(value in colNames for value in targetCols):
            dataManager.verboseOutput(self.verbouseOutput, "SAVING DATA IN CACHE FOR REDUCTION")
            dataManager.setSavedStructure(tableStructure)
            dataManager.setSavedData(tableData)
            dataManager.addToCache(tableData)
        else:
            dataManager.verboseOutput(self.verbouseOutput, "FOUND INCONSISTENT DECLARATION IN QUERY")
            raise ValueError("ATLEAST ONE OF THE TARGET TABLES DOES NOT EXIST IN " + targetTable)

    def exitUpdate_stmt(self, ctx: sqlParser.Update_stmtContext):
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TARGET TABLE FROM LEXER")

        targetTable = self.getTokenValue(ctx.table_name())

        colNames = [col[0] for col in dataManager.savedStructure]
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING EXPRETIONS FROM LEXER")

        exprs = [self.getTokenValue(expr) for expr in ctx.expr() if isinstance(expr, sqlParser.ExprLiteralValueContext)]
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TARGETS FROM LEXER")

        targets = [self.getTokenValue(col) for col in ctx.column_name()]
        targetsIndex = [colNames.index(elem) for elem in targets]

        dataManager.verboseOutput(self.verbouseOutput, "REDUCING DATA FOR UPDATE")

        untouchedData = [item for item in dataManager.cachedData[0] if item not in dataManager.savedData]
        reducedData = dataManager.savedData
        newData = []
        colTypes = [col[1] for col in dataManager.savedStructure]
        dataManager.verboseOutput(self.verbouseOutput, "GENERATING NEW DATA")

        for tup in reducedData:
            nTuple = []
            for i in range(0, len(tup)):
                if i in targetsIndex:
                    nTuple.append(dataManager.matchData(colTypes[i], exprs[i]))
                else:
                    nTuple.append(tup[i])
            newData.append(tuple(nTuple))
        dataManager.verboseOutput(self.verbouseOutput, "UPDATING DATA IN FILE SYSTEM")

        fileManager.insertTableFS(targetTable, str(newData + untouchedData))
        print("UPDATE DE " + targetTable + " EXITOSO")

    # ! UPDATE SECTION
    # DELETE SECTION
    def enterDelete_stmt(self, ctx: sqlParser.Delete_stmtContext):
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TARGET TABLE FROM LEXER")

        targetTable = self.getTokenValue(ctx.table_name())

        dataManager.verboseOutput(self.verbouseOutput, "EVALUATING TABLE AGAINST STRUCTURE DEFINED IN FILE SYSTEM")
        if targetTable not in fileManager.showTablesFS():
            raise ValueError("TABLE " + targetTable + " DOES NOT EXIST IN " + fileManager.currentDatabase)
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TABLE DATA FROM FILE SYSTEM")

        dataManager.verboseOutput(self.verbouseOutput, "SETTING DATA IN DATA MANAGER FOR REDUCTION")
        dataManager.setSavedData(eval(fileManager.readTableFS(targetTable, "data")))
        dataManager.addToCache(eval(fileManager.readTableFS(targetTable, "data")))
        dataManager.setSavedStructure(eval(fileManager.readTableFS(targetTable, "structure")))

    def exitDelete_stmt(self, ctx: sqlParser.Delete_stmtContext):
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TARGET TABLE FROM LEXER")

        targetTable = self.getTokenValue(ctx.table_name())

        dataManager.verboseOutput(self.verbouseOutput, "CALCULATING UNTOUCHED DATA")

        untouchedData = [item for item in dataManager.cachedData[0] if item not in dataManager.savedData]
        dataManager.verboseOutput(self.verbouseOutput, "SAVING REDUCED DATA IN FILE")

        fileManager.insertTableFS(targetTable, str(untouchedData))
        print("DELETE DE  " + targetTable + " EXITOSO")
        pass

    def exitParse(self, ctx: sqlParser.ParseContext):
        dataManager.verboseOutput(self.verbouseOutput, "SETTING DATA MANAGER VALUES TO DEFAULTS")

        dataManager.setSavedData([])
        dataManager.setSavedStructure([])
        dataManager.setCachedData([])
        dataManager.specificColsArray = []
        dataManager.multiples = False
        dataManager.verboseOutput(self.verbouseOutput, "EXECUTION ENDED")



    # ! DELETE SECTION

    # ORDER BY
    def enterOrdering_term(self, ctx: sqlParser.Ordering_termContext):
        dataManager.verboseOutput(self.verbouseOutput, "ORDER NODE DETECTED")
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING TARGET TABLE FROM LEXER")

        targetTable = [self.getTokenValue(ctx.expr())]
        dataManager.verboseOutput(self.verbouseOutput, "FETCHING COL NAMES FROM LEXER")

        colNames = [col[0] for col in dataManager.savedStructure]

        targetIndex = [colNames.index(elem) for elem in targetTable][0]
        # pdb.set_trace()
        dataManager.verboseOutput(self.verbouseOutput, "GENERATING AND SAVING ORDERED DATA IN MANAGER")

        dataManager.savedData = sorted(dataManager.savedData, key=lambda x: x[targetIndex])

    # ! ORDER BY
