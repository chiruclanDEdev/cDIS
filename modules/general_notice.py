from chiruserv import CSModules

class general_notice(CSModules):
	MODULE_CLASS = "NOTICE"
	
	def onData(self, data):
		if data.split()[2].startswith("#") and self.chanflag("l", data.split()[2]):
			self.log(data.split()[0][1:], "notice", data.split()[2], ' '.join(data.split()[3:]))