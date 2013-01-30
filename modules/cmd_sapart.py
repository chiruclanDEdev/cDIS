from chiruserv import CServMod

class cmd_sapart(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SAPART"
	HELP = "Forces a user to part a channel"
	NEED_OPER = 1

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			self.send(":"+self.bot+" SVSPART "+self.uid(arg[1])+" "+arg[0])
			self.msg(uid, "Done.")
		else:
			self.msg(uid, "Syntax: SAPART <#channel> <nick>")
