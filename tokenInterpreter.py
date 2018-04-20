from sqlListener import sqlListener
from dbFileManager import dbFileManager

import pdb

if __name__ is not None and "." in __name__:
    from .sqlParser import sqlParser
else:
    from sqlParser import sqlParser

fileManager = dbFileManager()


class tokenInterpreter(sqlListener):
    def __init__(self):
        pass

    def exitR(self, ctx):
        print("Hello world. At the input has been already validated")

    def getTokenValue(self, name):
        return name.any_name().IDENTIFIER().getText()

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
        print("current database changed to: " + datbase_name)
        fileManager.useDatabaseFS(datbase_name)

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
        cols = {}
        for column in ctx.column_def():
            cols[self.getTokenValue(column.column_name())] = self.getTokenValue(column.type_name().name()[0])
        # create database files
        if fileManager.createTableFS( table_name, cols):
            print("SE HA CREADO LA TABLA " + table_name + " EXITOSAMENTE")
        pass

    # !CREATE TABLE SECTION
    # SHOW TABLES SECTION
    def enterShow_tables_stmt(self, ctx: sqlParser.Show_tables_stmtContext):
        print("TABLES IN " + fileManager.getDatabaseFS())
        print(fileManager.showTablesFS())
        pass
    # SHOW TABLES SECTION
