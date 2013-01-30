from chiruserv import Module

class general_opertype(Module):
	MODULE_CLASS = "OPERTYPE"
	
	def onData(self, data):
		uid = data.split()[0][1:]
		self.query("insert into opers values (?)", uid)