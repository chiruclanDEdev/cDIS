from cDIS import cDISModule

class mod_3_part(cDISModule):
	MODULE_CLASS = "PART"
	BOT_ID = '3'
	
	def onData(self, data):
		arg = data.split()
		nick = arg[0][1:]
		chan = arg[2]
		
		self.query("delete from chanlist where channel = ? and uid = ?", chan, nick)