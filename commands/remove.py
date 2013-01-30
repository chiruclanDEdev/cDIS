from chiruserv import Module, config

class remove(Module):
	HELP = "Removes " + config.get("BOT", "nick") + " from your channel"
	NEED_AUTH = 1

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if self.getflag(source, arg[0]) == "n":
					for data in self.query("select name from channelinfo where name = ?", arg[0]):
						self.query("delete from channels where channel = ?", data["name"])
						self.query("delete from channelinfo where name = ?", data["name"])
						self.query("delete from banlist where channel = ?", data["name"])
						self.msg(source, "Channel {0} has been deleted.".format(escape_string(data["name"])))
						self.send(":{0} PART {1} :Channel {1} has been deleted.".format(self.bot, escape_string(data["name"])))
				else:
					self.msg(source, "No permission")
			else:
				self.msg(source, "Invalid channel: {0}".format(arg[0]))
		else:
			self.msg(source, "Syntax: REMOVE <#channel>")
