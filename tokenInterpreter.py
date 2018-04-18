from sqlListener import sqlListener
import pdb
if __name__ is not None and "." in __name__:
    from .sqlParser import sqlParser
else:
    from sqlParser import sqlParser


class tokenInterpreter(sqlListener):

    def __init__(self):
        pass

    def exitR(self, ctx):
        print("Hello world. At the input has been already validated")

    def getTokenValue(self, name):
        return name.any_name().IDENTIFIER()


# CREATE SECTION
    def enterCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        # print("Nombre de la tabla")
        databaseName = self.getTokenValue(ctx.database_name())
        print(databaseName)
    #     @TODO: IMPLEMENTAR CREADO DE CARPETA
    #     @TODO: IMPLEMENTAR CREADO DE DBS EN CARPETA

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