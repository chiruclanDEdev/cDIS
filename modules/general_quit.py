from chiruserv import CServMod

class general_quit(CServMod):
	MODULE_CLASS = "QUIT"
	
	def onData(self, data):
		for qchan in self.query("select * from chanlist where uid = ?", data.split()[0][1:]):
			if self.chanflag("l", qchan["channel"]):
				if len(data.split()) == 2:
					self.log(qchan["uid"], "quit", qchan["channel"])
				else:
					self.log(qchan["uid"], "quit", qchan["channel"], ' '.join(data.split()[2:])[1:])
					
		self.query("delete from chanlist where uid = ?", data.split()[0][1:])
		self.query("delete from temp_nick where nick = ?", str(data.split()[0])[1:])
		self.query("delete from gateway where uid = ?", str(data.split()[0])[1:])
		self.query("delete from online where uid = ?", str(data.split()[0])[1:])