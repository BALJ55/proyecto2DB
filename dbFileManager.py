from fileWorker import fileWorker


class dbFileManager():
    currentDatabase = ''
    dbSchemaTerm = '.schem'
    fileWorker = None

    def __init__(self):
        self.fileWorker = fileWorker()

    def createDatabaseFS(self, database):
        self.fileWorker.create_folder(database)
        self.fileWorker.createWrite_file(database+"/"+database+self.dbSchemaTerm,"[]")

    def useTableFS(self, database):
        self.currentDatabase = database
