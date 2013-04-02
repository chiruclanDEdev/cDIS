from cDIS import cDISModule

class cmd_1_notify(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "NOTIFY"
	HELP = "Sends a global notify to all users on the network"
	NEED_OPER = 1
	BOT_ID = '1'

	def onCommand(self, source, args):
		self.msg("$*", "[{nick}] {message}".format(nick=self.nick(source), message=args))
		self.msg(source, "Done.")