from sqlListener import sqlListener

if __name__ is not None and "." in __name__:
    from .sqlParser import sqlParser
else:
    from sqlParser import sqlParser


class tokenInterpreter(sqlListener):

    def __init__(self):
        print("Hoooli")

    def exitR(self, ctx):
        print("Hello world. At the input has been already validated")


# CREATE SECTION
    # Enter a parse tree produced by sqlParser#create_database_stmt.
    def enterCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        print(ctx)

    # Exit a parse tree produced by sqlParser#create_database_stmt.
    def exitCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        pass
# !CREATE SECTION