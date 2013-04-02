from cDIS import cDISModule

class mod_0_nick(cDISModule):
	MODULE_CLASS = "NICK"
	BOT_ID = '3'
	
	def onData(self, data):
		self.query("UPDATE `online` SET `nick` = ? WHERE `uid` = ?", data.split()[2], str(data.split()[0])[1:])