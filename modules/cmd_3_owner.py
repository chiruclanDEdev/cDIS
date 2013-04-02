from cDIS import cDISModule

class cmd_3_owner(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "OWNER"
	NEED_AUTH = 1
	HELP = "Sets your owner (+q) flag"
	BOT_ID = '3'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if self.getflag(source, arg[0]) == "n" or self.getflag(source, arg[0]) == "q":
					self.mode(arg[0], "+qo {0} {0}".format(source))
					self.msg(source, "Done.")
				else:
					self.msg(source, "Denied.")
			else:
				self.msg(source, "Invalid channel")
		else:
			self.msg(source, "Syntax: OWNER <#channel>")

	def onFantasy(self, uid, chan, args):
		flag = self.getflag(uid, chan)
		
		if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
			self.onCommand(uid, chan)
