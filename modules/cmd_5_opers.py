from cDIS import cDISModule

class cmd_5_opers(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "OPERS"
	HELP = "Shows all operators available for help"
	BOT_ID = '5'

	def onCommand(self, uid, args):
		self.msg(uid, "Available operators:")
		
		for data in self.query("select uid from opers"):
			self.msg(uid, "  "+self.nick(data["uid"]))
			
		self.msg(uid, "End of list.")
