from cDIS import cDISModule, bots

class cmd_2_remove(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "REMOVE"
	HELP = "Removes the channel service from your channel"
	NEED_AUTH = 1
	BOT_ID = '2'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if self.getflag(source, arg[0]) == "n":
					for data in self.query("select name from channelinfo where name = ?", arg[0]):
						self.query("delete from channels where channel = ?", data["name"])
						self.query("delete from channelinfo where name = ?", data["name"])
						self.query("delete from banlist where channel = ?", data["name"])
						self.msg(source, "Channel {0} has been deleted.".format(data["name"]))
						self.send(":{0} PART {1} :Channel {1} has been deleted.".format(self.services_id + bots.get("3", "uuid"), data["name"]))
				else:
					self.msg(source, "Denied.")
			else:
				self.msg(source, "Invalid channel: {0}".format(arg[0]))
		else:
			self.msg(source, "Syntax: REMOVE <#channel>")
