from cDIS import cDISModule

class cmd_suspend(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SUSPEND"
	HELP = "Suspends a channel"
	NEED_OPER = 1

	def onCommand(self, uid, args):
		arg = args.split()
		if len(arg) > 1:
			channel = arg[1]
		if len(arg) > 2:
			reason = ' '.join(arg[2:])
		
		if len(arg) == 2 and arg[0].lower() == "remove":
			if arg[1].startswith("#"):
				if self.suspended(channel):
					self.query("delete from suspended where channel = ?", channel)
					self.msg(uid, "Unsuspended.")
				else:
					self.msg(uid, arg[1]+" is not suspended.")
			else:
				self.msg(uid, "Invalid channel: "+arg[1])
		elif len(arg) > 2 and arg[0].lower() == "set":
			if arg[1].startswith("#"):
				if not self.suspended(channel):
					self.query("insert into suspended (`channel`, `reason`) values (?, ?)", channel, reason)
					
					if self.chanexist(channel):
						self.query("delete from channels where channel = ?", channel)
						self.query("delete from channelinfo where name = ?", channel)
						self.query("delete from banlist where channel = ?", channel)
						self.send(":{0} PART {1} :Channel {1} has been suspended.".format(self.bot, arg[1]))
						
					for user in self.userlist(channel):
						if not self.isoper(user):
							self.kick(arg[1], user, "Suspended: "+' '.join(arg[2:]))
						else:
							self.msg(arg[1], "This channel is suspended: "+' '.join(arg[2:]))
				else:
					self.query("update suspended set reason = ? where channel = ?", reason, channel)
					
					for user in self.userlist(channel):
						if not self.isoper(user):
							self.kick(arg[1], user, "Suspended: "+' '.join(arg[2:]))
						else:
							self.msg(arg[1], "This channel is suspended: "+' '.join(arg[2:]))
							
				self.msg(uid, "Suspended.")
			else:
				self.msg(uid, "Invalid channel: "+arg[1])
		elif len(arg) == 1 and arg[0].lower() == "list":
			for data in self.query("select * from suspended"):
				self.msg(uid, "Channel: {0} {1} Reason: {2}".format(data["channel"], " "*int(23-len(data["channel"])), data["reason"]))
		else:
			self.msg(uid, "Syntax: SUSPEND <list/set/remove> <#channel> [<reason>]")
