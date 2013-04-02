from cDIS import cDISModule

class 3_mod_kick(cDISModule):
	MODULE_CLASS = "KICK"
	BOT_ID = '3'
	
	def onData(self, data):
		arg = data.split()
		knick = arg[0][1:]
		kchan = arg[2]
		ktarget = self.uid(arg[3])
		kreason = ' '.join(arg[4:])[1:]
		
		if ktarget == self.bot:
			self.join(kchan)
		else:
			self.query("delete from chanlist where channel = ? and uid = ?", kchan, ktarget)