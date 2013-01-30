from chiruserv import CServMod

class cmd_chanmode(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "CHANMODE"
	HELP = "Sets modes for your channel"
	NEED_AUTH = 1

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if self.getflag(source, arg[0]) == "n" or self.getflag(source, arg[0]) == "q" or self.getflag(source, arg[0]) == "a":
					for channel in self.query("select name,modes from channelinfo where name = ?", arg[0]):
						self.msg(source, "Current modes for {0}: {1}".format(channel["name"], channel["modes"]))
				else:
					self.msg(source, "Denied.")
			else:
				self.msg(source, "Invalid channel '{0}'".format(arg[0]))
		elif len(arg) == 2:
			modes = arg[1]
			
			if arg[0].startswith("#"):
				if self.getflag(source, arg[0]) == "n" or self.getflag(source, arg[0]) == "q" or self.getflag(source, arg[0]) == "a":
					for channel in self.query("select name,modes from channelinfo where name = ?", arg[0]):
						modes = self.regexflag(channel["modes"], modes, True)
						self.query("update channelinfo set modes = ? where name = ?", modes, channel["name"])
						self.mode(channel["name"], modes)
						self.msg(source, "Done. New modes for {0}: {1}".format(channel["name"], modes))
				else:
					self.msg(source, "Denied.")
			else:
				self.msg(source, "Invalid channel '{0}'".format(arg[0]))
		else:
			self.msg(source, "Syntax: CHANMODE <#channel> [<modes>]")

	def onFantasy(self, uid, chan, args):
		flag = self.getflag(uid, chan)
		
		if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
			self.onCommand(uid, chan + " " + args)
