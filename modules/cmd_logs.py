from chiruserv import CServMod

class cmd_logs(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "LOGS"
	HELP = "View and clear channel logs"
	NEED_AUTH = 1
	
	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			if arg[0].startswith("#"):
				flag = self.getflag(uid, arg[0])
				
				if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
					if arg[1].lower() == "view":
						self.showlog(uid, arg[0])
					elif arg[1].lower() == "clear":
						if flag == "n" or flag == "q" or flag == "a":
							self.query("DELETE FROM `logs` WHERE `channel` = ?", arg[0])
							self.msg(uid, "Done.")
						else:
							self.msg(uid, "Denied.")
					else:
						self.msg(uid, "Syntax: LOGS <#channel> <view/clear>")
				else:
					self.msg(uid, "Denied.")
		else:
			self.msg(uid, "Syntax: LOGS <#channel> <view/clear>")
			
	def onFantasy(self, uid, chan, args):
		self.query("DELETE FROM `logs` WHERE `channel` = ? AND `action` = 'PRIVMSG' AND `message` = ?", chan, self.fantasy(chan) + "logs view")
		self.onCommand(uid, chan + " " + args)