from chiruserv import CSModules

class notify(CSModules):
	HELP = "Sends a global notify to all users on the network"
	NEED_OPER = 1

	def onCommand(self, source, args):
		self.msg("$*", "[{nick}] {message}".format(nick=self.nick(source), message=args))
		self.msg(source, "Done.")