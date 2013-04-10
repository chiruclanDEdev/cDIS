from cDIS import cDISModule

class cmd_2_request(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "REQUEST"
	HELP = "Requests the channel service for your channel"
	NEED_AUTH = 1
	BOT_ID = '2'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if not self.chanexist(arg[0]):
					if not self.suspended(arg[0]):
						if self.channelusercount(arg[0]) >= 10:
							self.query("insert into channelinfo values (?, '', '', '', '', '10:5', '!')", arg[0])
							self.query("insert into channels values (?, ?, 'n')", arg[0], self.auth(source))
							self.join(arg[0])
							self.mode(arg[0], "+qo {0} {0}".format(source))
							self.msg(source, "Channel %s has been registered for you" % arg[0])
						else:
							self.msg(source, "This channel does not meet the requirements. Please try again later.")
					else:
						self.msg(source, "Channel " + arg[0] + " is suspended: " + self.suspended(arg[0]))
				else:
					self.msg(source, "Channel %s is already registered" % arg[0])
			else:
				self.msg(source, "Invalid channel: {0}".format(arg[0]))
		else:
			self.msg(source, "Syntax: REQUEST <#channel>")
