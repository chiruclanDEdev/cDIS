from cDIS import cDISModule, config

class cmd_newpass(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "NEWPASS"
	HELP = "Changes your password at " + config.get("BOT", "nick") + "@" + config.get("SERVICES", "name")
	NEED_AUTH = 1

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			self.query("update users set pass = ? where name = ?", self.encode(arg[0]), self.auth(source))
			self.msg(source, """Your new password is "%s". Remember it!""" % arg[0])
		else:
			self.msg(source, "Syntax: NEWPASS <password>")
