from pyserv import Command

class owner(Command):
	nauth = 1
	help = "Sets your owner (+q) flag"
	def onCommand(self, source, args):
		arg = args.split()
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if self.getflag(source, arg[0]) == "n" or self.getflag(source, arg[0]) == "q":
					self.mode(arg[0], "+q {0}".format(source))
					self.msg(source, "Done.")
				else: self.msg(source, "Denied.")
			else: self.msg(source, "Invalid channel")
		else: self.msg(source, "Syntax: OWNER <#channel>")

	def onFantasy(self, uid, chan, args):
		self.onCommand(uid, chan)
