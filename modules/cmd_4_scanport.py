from cDIS import cDISModule

class cmd_4_scanport(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SCANPORT"
	HELP = "Checks host for an open port"
	NEED_OPER = 1
	BOT_ID = '4'

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			self.msg(uid, "Scanning " + arg[0] + ":" + arg[1] + " ...")
			
			if self.scanport(arg[0], arg[1]):
				self.msg(uid, arg[0] + ":" + arg[1] + ": Open.")
			else:
				self.msg(uid, arg[0] + ":" + arg[1] + ": Closed.")
		else:
			self.msg(uid, "Syntax: SCANPORT <host> <port>")