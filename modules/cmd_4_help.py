from cDIS import cDISModule

class cmd_4_help(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "HELP"
	HELP = "Shows help"
	BOT_ID = '4'
	
	def onCommand(self, source, args):
		self.msg(source, "The following commands are available to you.")
		
		if len(args) == 0:
			for command in self.query("SELECT * FROM `modules` WHERE `class` = 'COMMAND' AND `bot` = ? ORDER BY `command`", BOT_ID):
				if os.access("modules/"+command["name"]+".py", os.F_OK):
					cmd_auth = command["auth"]
					cmd_help = command["help"]
					
					if not cmd_auth:
						self.help(source, command["command"], cmd_help)
					elif cmd_auth and self.auth(source):
						self.help(source, command["command"], cmd_help)
		else:
			for command in self.query("SELECT * FROM `modules` WHERE `class` = 'COMMAND' AND `bot` = ? AND `command` LIKE ?", '%' + args + '%'):
				if os.access("modules/"+command["name"]+".py", os.F_OK):
					cmd_auth = command["auth"]
					cmd_help = command["help"]
					
					if not cmd_auth:
						self.help(source, command["command"], cmd_help)
					elif cmd_auth and self.auth(source):
						self.help(source, command["command"], cmd_help)
		
		self.msg(source, "End of list.")