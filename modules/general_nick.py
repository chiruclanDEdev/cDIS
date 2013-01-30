from chiruserv import Module

class general_nick(Module):
	MODULE_CLASS = "NICK"
	
	def onData(self, data):
		self.query("update online set nick = ? where uid = ?", data.split()[2], str(data.split()[0])[1:])