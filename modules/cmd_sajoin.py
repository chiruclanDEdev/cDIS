from chiruserv import CServMod

class cmd_sajoin(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SAJOIN"
	HELP = "Forces a user to join a channel"
	NEED_OPER = 1

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			self.send(":"+self.bot+" SVSJOIN "+self.uid(arg[1])+" "+arg[0])
			self.msg(uid, "Done.")
		else:
			self.msg(uid, "Syntax: SAJOIN <#channel> <nick>")