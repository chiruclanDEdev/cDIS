from cDIS import cDISModule

class mod_0_metadata(cDISModule):
	MODULE_CLASS = "METADATA"
	
	def onData(self, data):
		if len(data.split()) == 5 and len(data.split()[4]) != 1:
			uid = data.split()[2]
			string = data.split()[3]
			content = ' '.join(data.split()[4:])[1:]
			self.metadata(uid, string, content)