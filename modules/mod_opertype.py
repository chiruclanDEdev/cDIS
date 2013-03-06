from cDIS import cDISModule

class mod_opertype(cDISModule):
	MODULE_CLASS = "OPERTYPE"
	
	def onData(self, data):
		uid = data.split()[0][1:]
		type = data.split()[2]
		self.query("DELETE FROM `opers` WHERE `uid` = ?", uid)
		self.query("INSERT INTO `opers` (`uid`, `opertype`) VALUES (?, ?)", uid, type)