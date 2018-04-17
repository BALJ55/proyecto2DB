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


# CREATE SECTION
    def enterCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        print("Nombre de la tabla")
        databaseName = ctx.database_name().any_name().IDENTIFIER()
    #     @TODO: IMPLEMENTAR CREADO DE CARPETA

    def exitCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        pass
# !CREATE SECTION