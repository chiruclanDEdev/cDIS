import pyserv

class invite(pyserv.Command):
	help="Invites you into a channel"
	auth = 1
	def onCommand(self, source, args):
		arg = args.split()
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if self.getflag(source, arg[0]) != 0:
					self.send(":{0} INVITE {1} {2}".format(self.bot, source, arg[0]))
					self.msg(source, "Done.")
				else: self.msg(source, "Denied.")
			else: self.msg(source, "Invalid channel")
		else: self.msg(source, "Syntax: INVITE <#channel>")
