from pyserv import Command

class sajoin(Command):
	help = "Forces a user to join a channel"
	oper = 1
	def onCommand(self, uid, args):
		arg = args.split()
		if len(arg) == 2:
			self.send(":"+self.bot+" SVSJOIN "+self.uid(arg[0])+" "+arg[1])
			self.msg(uid, "Done.")
		else:
			self.msg(uid, "Syntax: SAJOIN <nick> <#channel>")
