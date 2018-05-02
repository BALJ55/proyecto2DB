from fileWorker import fileWorker
import collections  # ordered dictionary
import json  # OD decoder


class dbFileManager():
    currentDatabase = None
    dbSchemaTerm = '.schem'
    dbInfoTerm = '.dat'
    fileWorker = None

    def __init__(self):
        self.fileWorker = fileWorker()

    def createDatabaseFS(self, database):
        self.fileWorker.create_folder(database)

    def showDatabasesFS(self):
        return self.fileWorker.list_files()

    def showTablesFS(self):
        if self.currentDatabase is not None:
            return self.fileWorker.list_files(self.currentDatabase)
        else:
            raise TypeError("A DATABASE HAS NOT BEEN SELECTED")

    def removeDatabaseFS(self, database):
        self.fileWorker.remove_folder(database)

    def createTableFS(self, table_name, table_structure):
        if (self.currentDatabase):
            self.fileWorker.create_folder(self.currentDatabase + "/" + table_name)  # crear carpeta de la tabla
            self.fileWorker.createWrite_file(
                self.currentDatabase + "/" + table_name + "/" + table_name + self.dbSchemaTerm,
                json.dumps(table_structure))  # crear schema con la estructura de la tabla

            self.fileWorker.createWrite_file(
                self.currentDatabase + "/" + table_name + "/" + table_name + self.dbInfoTerm,
                "[]")  # crear array vacío para información de la tabla
            return True
        else:
            raise ValueError('THE DATABASE WAS NOT SELECTED')

    def useDatabaseFS(self, database):
        if database not in self.showDatabasesFS():
            raise ValueError(database + " DOES NOT EXIST IN THE DATABASE")
        self.currentDatabase = database

    def getDatabaseFS(self):
        return self.currentDatabase

    def insertTableFS(self, table, data):
        self.fileWorker.createWrite_file(self.currentDatabase + "/" + table + "/" + table + self.dbInfoTerm, data)

    def readTableFS(self, table, fileType):
        return self.fileWorker.read_file(self.currentDatabase + "/" + table + "/" + table + (self.dbInfoTerm if fileType == "data" else self.dbSchemaTerm))

    def renameFS(self, table_name_old, table_name_new):
        return self.fileWorker.rename_files(self.currentDatabase + "/", self.currentDatabase + "/" + table_name_old + "/", table_name_old, table_name_new)

    def updateFS(self, table, fileType):
        return self.fileWorker.read_file(self.currentDatabase + "/" + table + "/" + table + (self.dbInfoTerm if fileType == "data" else self.dbSchemaTerm))