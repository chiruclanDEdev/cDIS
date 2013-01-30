from chiruserv import CSModules

class general_nick(CSModules):
	MODULE_CLASS = "NICK"
	
	def onData(self, data):
		self.query("update online set nick = ? where uid = ?", data.split()[2], str(data.split()[0])[1:])