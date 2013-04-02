from cDIS import cDISModule

class 3_cmd_sync(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SYNC"
	NEED_AUTH = 1
	HELP = "Syncs your flags on all channels"
	BOT_ID = '3'

	def onCommand(self, source, args):
		self.flag(source)
		self.msg(source, "Done.")