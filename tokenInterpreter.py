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

    # CREATE SECTION
    def enterCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        database_name = self.getTokenValue(ctx.database_name())
        fileManager.createDatabaseFS(database_name)

    def exitCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        print("DATABASE CREATE EXECUTED")
        pass

    # !CREATE SECTION
    # ALTER TABLE SECTION
    def enterAlter_database_stmt(self, ctx: sqlParser.Alter_database_stmtContext):
        target_database = ctx.database_name().any_name().IDENTIFIER()
        pass

    def exitAlter_database_stmt(self, ctx: sqlParser.Alter_database_stmtContext):
        pass

    # !ALTER TABLE SECTION
    # USE DATABASE SECION
    def enterUse_database_stmt(self, ctx: sqlParser.Use_database_stmtContext):
        datbase_name = self.getTokenValue(ctx.database_name())
        fileManager.useDatabaseFS(datbase_name)
        pass

    def exitUse_database_stmt(self, ctx: sqlParser.Use_database_stmtContext):
        pass
    # !USE DATABASE SECION
