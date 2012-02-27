from pyserv import Command
from fnmatch import fnmatch

class dehalfop(Command):
	help = "Removes halfop (+h) flag from you or someone on the channel"
	nauth = 1
	def onCommand(self, source, args):
		arg = args.split()
		if len(arg) == 1:
			if arg[0].startswith("#"):
				flag = self.getflag(source, arg[0])
				if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
					self.mode(arg[0], "-h {0}".format(source))
					self.msg(source, "Done.")
				else: self.msg(source, "Denied.")
			else: self.msg(source, "Invalid channel")
		elif len(arg) == 2:
			if arg[0].startswith("#"):
				flag = self.getflag(source, arg[0])
				if flag == "n" or flag == "q" or flag == "a" or flag == "o":
					for user in self.userlist(arg[0]):
						if fnmatch(self.nick(user), arg[1]):
							self.mode(arg[0], "-h "+user)
							if self.chanflag("p", arg[0]):
								uflag = self.getflag(user, arg[0])
								if uflag == "h":
									self.mode(arg[0], "+h "+user)
					self.msg(source, "Done.")
				else: self.msg(source, "Denied.")
			else: self.msg(source, "Invalid channel")
		else: self.msg(source, "Syntax: DEHALFOP <#channel> [<nick> [<nick>]]")

	def onFantasy(self, uid, chan, args):
		self.onCommand(uid, chan + " " + args)
