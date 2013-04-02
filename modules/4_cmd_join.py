from cDIS import cDISModule

class 4_cmd_join(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "JOIN"
	HELP = "Forces a user to join a channel"
	NEED_OPER = 1
	BOT_ID = '4'

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			self.send(":"+self.bot+" SVSJOIN "+self.uid(arg[1])+" "+arg[0])
			self.msg(uid, "Done.")
		else:
			self.msg(uid, "Syntax: SAJOIN <#channel> <nick>")
