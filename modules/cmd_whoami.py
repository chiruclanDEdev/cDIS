from chiruserv import CServMod

class cmd_whoami(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "WHOAMI"
	HELP = "Shows information about you"
	NEED_AUTH = 1

	def onCommand(self, source, args):
		auth = self.auth(source)
		
		for user in self.query("select name,email from users where name = ?", auth):
			self.msg(source, "-Information for account {0}:".format(user["name"]))
			online = list()
			
			for uid in self.sid(user["name"]):
				online.append(self.nick(uid))
				
			self.msg(source, "Online Nicks  : {0}".format(' '.join(online)))
			self.msg(source, "User flags    : +{0}".format(self.userflags(user["name"])))
			self.msg(source, "Email address : {0}".format(user["email"]))
			self.msg(source, "vHost         : {0}".format(self.getvhost(user["name"])))
			self.msg(source, "Gateway       : {0}".format(str(self.gateway(source))))
			self.msg(source, "Known on following channels:")
			self.msg(source, "Channel              Flag")
			
			for channel in self.query("select channel,flag from channels where user = ? order by flag,channel", user["name"]):
				self.msg(source, " {0}{1}+{2}".format(channel["channel"], " "*int(20-len(channel["channel"])), channel["flag"]))
				
			self.msg(source, "End of list.")