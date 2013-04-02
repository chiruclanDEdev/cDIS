from cDIS import cDISModule

class mod_0_idle(cDISModule):
	MODULE_CLASS = "IDLE"
	
	def onData(self, data):
		if len(data.split()) == 3:
			self.send(":{uid} IDLE {source} 0 0".format(uid=data.split()[2], source=data.split()[0][1:]))