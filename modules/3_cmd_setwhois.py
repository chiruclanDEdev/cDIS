from cDIS import cDISModule

class 3_cmd_setwhois(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SETWHOIS"
	HELP = "Sets cool stuff in your whois"
	NEED_AUTH = 1
	BOT_ID = '3'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) > 0:
			self.send(":{uid} SWHOIS {target} :{text}".format(uid=self.bot, target=source, text=' '.join(arg[0:])))
			self.msg(source, "Done.")
		else:
			self.send(":{uid} SWHOIS {target} :".format(uid=self.bot, target=source))
			self.msg(source, "Done.")