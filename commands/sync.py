from chiruserv import CServMod

class sync(CServMod):
	NEED_AUTH = 1
	HELP = "Syncs your flags on all channels"

	def onCommand(self, source, args):
		self.flag(source)
		self.msg(source, "Done.")