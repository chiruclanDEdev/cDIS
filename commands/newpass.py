from pyserv import Command

class newpass(Command):
	help = "Changes your password at Q@"+pyserv.config.get("SERVICES", "name")
	nauth = 1
	def onCommand(self, source, args):
		arg = args.split()
		if len(arg) == 1:
			self.query("update users set pass = '%s' where name = '%s'" % (self.hash(arg[0]), self.auth(source)))
			self.msg(source, """Your new password is "%s". Remember it!""" % arg[0])
		else:
			self.msg(source, "Syntax: NEWPASS <password>")
