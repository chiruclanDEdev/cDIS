from cDIS import cDISModule

class cmd_4_kill(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "KILL"
	HELP = "Kills a user from the network"
	NEED_OPER = 1
	BOT_ID = '4'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			self.kill(arg[0])
			self.msg(source, "Done.")
		elif len(arg) > 1:
			self.kill(arg[0], ' '.join(arg[1:]))
			self.msg(source, "Done.")
		else:
			self.msg(source, "Syntax: KILL <nick> [<reason>]")
