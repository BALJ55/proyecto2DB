from sqlListener import sqlListener
from dbFileManager import dbFileManager

import pdb

if __name__ is not None and "." in __name__:
    from .sqlParser import sqlParser
else:
    from sqlParser import sqlParser

fileManager = dbFileManager()


class tokenInterpreter(sqlListener):
    currentDatabase = None

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

        pass

    def exitShow_databases_stmt(self, ctx: sqlParser.Show_databases_stmtContext):
        pass
    # !SHOW DATABASE SECTION
    # USE DATABASE SECION
    def enterUse_database_stmt(self, ctx: sqlParser.Use_database_stmtContext):
        datbase_name = self.getTokenValue(ctx.database_name())
        print("current database changed to: " + datbase_name)
        self.currentDatabase = datbase_name
        pass

    def exitUse_database_stmt(self, ctx: sqlParser.Use_database_stmtContext):
        pass

    # !USE DATABASE SECION
    # DROP DATABASE SECTION
    def enterDrop_database_stmt(self, ctx: sqlParser.Drop_database_stmtContext):
        database_name = self.getTokenValue(ctx.database_name())
        fileManager.removeDatabaseFS(database_name)
        pass

    def exitDrop_database_stmt(self, ctx: sqlParser.Drop_database_stmtContext):
        pass

    # !DROP DATABASE SECTION

    # CREATE TABLE SECTION
    def enterCreate_table_stmt(self, ctx: sqlParser.Create_table_stmtContext):
        table_name = self.getTokenValue(ctx.table_name())
        cols = {}
        for column in ctx.column_def():
            cols[self.getTokenValue(column.column_name())] = self.getTokenValue(column.type_name().name()[0])
        # create database files
        if(fileManager.createTableFS(self.currentDatabase,table_name, cols)):
            print("SE HA CREADO LA TABLA " + table_name + " EXITOSAMENTE")
        pass

    def exitCreate_table_stmt(self, ctx: sqlParser.Create_table_stmtContext):
        pass
    # !CREATE TABLE SECTION
