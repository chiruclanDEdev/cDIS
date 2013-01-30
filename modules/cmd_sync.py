from chiruserv import CServMod

class cmd_sync(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SYNC"
	NEED_AUTH = 1
	HELP = "Syncs your flags on all channels"

	def onCommand(self, source, args):
		self.flag(source)
		self.msg(source, "Done.")