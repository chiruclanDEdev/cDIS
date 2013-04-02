from cDIS import cDISModule

class mod_3_notice(cDISModule):
	MODULE_CLASS = "NOTICE"
	BOT_ID = '3'
	
	def onData(self, data):
		if data.split()[2].startswith("#") and self.chanflag("l", data.split()[2]):
			self.log(data.split()[0][1:], "notice", data.split()[2], ' '.join(data.split()[3:]))