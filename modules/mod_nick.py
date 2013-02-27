from chiruserv import CServMod

class mod_nick(CServMod):
	MODULE_CLASS = "NICK"
	
	def onData(self, data):
		self.query("UPDATE `online` SET `nick` = ? WHERE `uid` = ?", data.split()[2], str(data.split()[0])[1:])