import pyserv

class newpass(pyserv.Command):
	help = ""
	auth = 1
	def onCommand(self, source, args):
		arg = args.split()
		if len(arg) == 1:
			self.msg(source, str(self.auth(source)))
			self.query("update users set pass = '%s' where name = '%s'" % (self.hash(arg[0]), self.auth(source)))
			self.msg(source, """Your new password is "%s". Remember it!""" % arg[0])
		else:
			self.msg(source, "Syntax: NEWPASS <password>")