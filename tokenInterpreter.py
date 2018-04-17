from sqlListener import sqlListener

class tokenInterpreter(sqlListener):

	def __init__(self):
		print("Hoooli")
	def exitR(self, ctx):
		print("Hello world. At the input has been already validated")