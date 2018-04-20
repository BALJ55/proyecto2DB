from fileWorker import fileWorker


class dbFileManager():
    currentDatabase = ''
    dbSchemaTerm = '.schem'
    dbInfoTerm = '.dat'
    fileWorker = None

    def __init__(self):
        self.fileWorker = fileWorker()

    def createDatabaseFS(self, database):
        self.fileWorker.create_folder(database)

    def useDatabaseFS(self, database):
        print("current database changed to: "+database)
        self.currentDatabase = database

