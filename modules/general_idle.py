from chiruserv import CServMod

class general_idle(CServMod):
	MODULE_CLASS = "IDLE"
	
	def onData(self, data):
		if len(data.split()) == 3:
			self.send(":{uid} IDLE {source} 0 0".format(uid=data.split()[2], source=data.split()[0][1:]))