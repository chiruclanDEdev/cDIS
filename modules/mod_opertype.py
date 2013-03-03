from chiruserv import CServMod

class mod_opertype(CServMod):
	MODULE_CLASS = "OPERTYPE"
	
	def onData(self, data):
		uid = data.split()[0][1:]
		type = data.split()[2]
		self.query("INSERT INTO `opers` (`uid`, `opertype`) VALUES (?, ?)", uid, type)