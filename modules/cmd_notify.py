from chiruserv import CServMod

class cmd_notify(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "NOTIFY"
	HELP = "Sends a global notify to all users on the network"
	NEED_OPER = 1

	def onCommand(self, source, args):
		self.msg("$*", "[{nick}] {message}".format(nick=self.nick(source), message=args))
		self.msg(source, "Done.")