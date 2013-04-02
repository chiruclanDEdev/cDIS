from cDIS import cDISModule

class 4_cmd_mode(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "MODE"
	HELP = "Change modes on a channel where you have no rights"
	NEED_OPER = 1
	BOT_ID = '4'

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) > 1:
			if arg[0].startswith("#"):
				self.mode(arg[0], ' '.join(arg[1:]))
				self.msg(uid, "Done.")
			else:
				self.msg(uid, "Invalid channel: " + arg[0])
		else:
			self.msg(uid, "Syntax: SAMODE <#channel> <modes>")
