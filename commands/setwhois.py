from chiruserv import CSModules

class setwhois(CSModules):
	HELP = "Sets cool stuff in your whois"
	NEED_AUTH = 1

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) > 0:
			self.send(":{uid} SWHOIS {target} :{text}".format(uid=self.bot, target=source, text=' '.join(arg[0:])))
			self.msg(source, "Done.")
		else:
			self.send(":{uid} SWHOIS {target} :".format(uid=self.bot, target=source))
			self.msg(source, "Done.")