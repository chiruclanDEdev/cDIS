from cDIS import cDISModule

class cmd_feedback(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "FEEDBACK"
	HELP = "Sends your feedback about us to us"
	NEED_AUTH = 1

	def onCommand(self, source, args):
		
		if len(args) > 0:
			entry = False
			
			for data in self.query("select text from feedback where user = ?", self.auth(source)):
				entry = True
				
			if not entry:
				self.query("insert into feedback values(?, ?)", self.auth(source), args)
				self.msg(source, "Feedback added to queue.")
				
				for op in self.query("select uid from opers"):
					self.msg(str(op["uid"]), "New feedback from %s" % self.auth(source))
			else:
				self.msg(source, "You already sent a feedback. Please wait until an operator read it.")
		else:
			self.msg(source, "FEEDBACK <text>")
