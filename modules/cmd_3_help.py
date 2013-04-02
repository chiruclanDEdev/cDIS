from cDIS import cDISModule
import os

class cmd_3_help(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "HELP"
	HELP = "Shows help"
	BOT_ID = '3'
	
	def onCommand(self, source, args):
		arg = args.split()
		
		self.msg(source, "The following commands are available to you.")
		
		if len(arg) == 0:
			for command in self.query("SELECT * FROM `modules` WHERE `class` = 'COMMAND' AND `bot` = ? ORDER BY `command`", self.BOT_ID):
				if os.access("modules/"+command["name"]+".py", os.F_OK):
					cmd_auth = int(command["auth"])
					cmd_help = command["help"]
					cmd_oper = (command["oper"])
					
					if cmd_oper == 0:
						if cmd_auth == 0:
							self.help(source, command["command"], cmd_help)
						elif cmd_auth == 1 and self.auth(source) != 0:
							self.help(source, command["command"], cmd_help)
					elif cmd_oper == 1 and self.isoper(source):
						self.help(source, command["command"], cmd_help)
		else:
			for command in self.query("SELECT * FROM `modules` WHERE `class` = 'COMMAND' AND `bot` = ? AND `command` LIKE ? ORDER BY `command`", self.BOT_ID, '%' + args + '%'):
				if os.access("modules/"+command["name"]+".py", os.F_OK):
					cmd_auth = int(command["auth"])
					cmd_help = command["help"]
					cmd_oper = int(command["oper"])
					
					if cmd_oper == 0:
						if cmd_auth == 0:
							self.help(source, command["command"], cmd_help)
						elif cmd_auth == 1 and self.auth(source) != 0:
							self.help(source, command["command"], cmd_help)
					elif cmd_oper == 1 and self.isoper(source):
						self.help(source, command["command"], cmd_help)
		
		self.msg(source, "End of list.")

	def onFantasy(self, source, channel, args):
		self.onCommand(source, args)