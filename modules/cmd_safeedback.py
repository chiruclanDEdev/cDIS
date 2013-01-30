from chiruserv import CServMod

class cmd_safeedback(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SAFEEDBACK"
	HELP = "Reads the feedback from users"
	NEED_OPER = 1

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(args) == 0:
			self.msg(source, "Following users sent a feedback:")
			
			for data in self.query("select user from feedback"):
				self.msg(source, "  "+str(data["user"]))
				
			self.msg(source, "To read a feedback: SAFEEDBACK <user>")
		else:
			entry = False
			
			for data in self.query("select user,text from feedback where user = ?", arg[0]):
				entry = True
				self.msg(source, "[Feedback] From: %s, Message: %s" % (data["user"], data["text"]))
				self.query("delete from feedback where user = ?", str(data["user"]))
				
			if not entry:
				self.msg(source, "There is no feedback from %s" % arg[0])
