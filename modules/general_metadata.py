from chiruserv import CServMod

class general_metadata(CServMod):
	MODULE_CLASS = "METADATA"
	
	def onData(self, data):
		if len(data.split()) == 5 and len(data.split()[4]) != 1:
			uid = data.split()[2]
			string = data.split()[3]
			content = ' '.join(data.split()[4:])[1:]
			self.metadata(uid, string, content)