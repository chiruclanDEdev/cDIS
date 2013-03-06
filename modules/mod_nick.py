from cDIS import cDISModule

class mod_nick(cDISModule):
	MODULE_CLASS = "NICK"
	
	def onData(self, data):
		self.query("UPDATE `online` SET `nick` = ? WHERE `uid` = ?", data.split()[2], str(data.split()[0])[1:])