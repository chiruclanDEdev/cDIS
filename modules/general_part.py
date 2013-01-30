from chiruserv import CServMod

class general_part(CServMod):
	MODULE_CLASS = "PART"
	
	def onData(self, data):
		pnick = data.split()[0][1:]
		pchan = data.split()[2]
		
		for parted in self.query("select channel from ipchan where ip = ? and channel = ?", self.getip(pnick), pchan):
			self.send(":%s SVSJOIN %s %s" % (self.bot, pnick, parted["channel"]))
			self.msg(pnick, "Your IP is forced to be in "+parted["channel"])
			
		self.query("delete from chanlist where uid = ? and channel = ?", pnick, pchan)
		
		if self.chanflag("l", pchan):
			if len(data.split()) == 3:
				self.log(pnick, "part", pchan)
			else:
				self.log(pnick, "part", pchan, ' '.join(data.split()[3:])[1:])