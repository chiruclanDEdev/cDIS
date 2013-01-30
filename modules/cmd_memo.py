from chiruserv import CServMod

class cmd_memo(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "MEMO"
	HELP = "Send another user a memo"
	NEED_AUTH = 1

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) > 1:
			if arg[0].startswith("#"):
				user = arg[0][1:]
				
				if self.user(user):
					sender = self.auth(source)
					message = ' '.join(arg[1:])
					self.query("insert into memo (`user`, `source`, `message`) values (?, ?, ?)", user, sender, message)
					self.msg(source, "Done.")
					self.memo(user)
				else:
					self.msg(source, "Can't find user %s." % arg[0])
			else:
				user = self.auth(arg[0])
				
				if self.user(user):
					sender = self.auth(source)
					message = ' '.join(arg[1:])
					self.query("insert into memo (`user`, `source`, `message`) values (?, ?, ?)", user, sender, message)
					self.msg(source, "Done.")
					self.memo(user)
				else:
					self.msg(source, "Can't find user %s." % arg[0])
		else:
			self.msg(source, "Syntax: MEMO <user> <message>")
