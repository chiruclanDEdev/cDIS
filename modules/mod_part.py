from chiruserv import CServMod

class mod_part(CServMod):
	MODULE_CLASS = "PART"
	
	def onData(self, data):
		arg = data.split()
		nick = arg[0][1:]
		chan = arg[2]
		
		self.query("delete from chanlist where channel = ? and uid = ?", chan, nick)