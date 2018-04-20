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
            raise TypeError("NO SE HA SELECCIONADO UNA BASE DE DATOS")

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
            raise ValueError('NO SE HA SELECCIONADO LA BASE DE DATOS')

    def readTableFS(self, table_name):
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)

    def useDatabaseFS(self, database):
        self.currentDatabase = database
    def getDatabaseFS(self):
        return self.currentDatabase
