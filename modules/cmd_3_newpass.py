from cDIS import cDISModule, config, bots

class cmd_3_newpass(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "NEWPASS"
	HELP = "Changes your password at " + bots.get("3", "nick") + "@" + config.get("SERVICES", "name")
	NEED_AUTH = 1
	BOT_ID = '3'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			self.query("update users set pass = ? where name = ?", self.encode(arg[0]), self.auth(source))
			self.msg(source, """Your new password is "%s". Remember it!""" % arg[0])
		else:
			self.msg(source, "Syntax: NEWPASS <password>")
