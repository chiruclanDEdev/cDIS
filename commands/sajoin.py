from chiruserv import CServMod

class sajoin(CServMod):
	HELP = "Forces a user to join a channel"
	NEED_OPER = 1

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			self.send(":"+self.bot+" SVSJOIN "+self.uid(arg[1])+" "+arg[0])
			self.msg(uid, "Done.")
		else:
			self.msg(uid, "Syntax: SAJOIN <#channel> <nick>")
