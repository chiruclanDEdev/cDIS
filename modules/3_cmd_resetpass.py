from cDIS import cDISModule
from time import time

class 3_cmd_resetpass(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "RESETPASS"
	HELP = "Reset your lost password"
	BOT_ID = '3'

	def onCommand(self, uid, args):
		if self.auth(uid) == 0:
			arg = args.split()
			
			if len(arg) == 2:
				entry = False
				
				for data in self.query("select name,pass,email,suspended from users where name = ? and email = ?", arg[0], arg[1]):
					entry = True
					
					if data["suspended"] == "0":
						newpw = str(hash(str(time()) + data["name"] + data["pass"] + data["email"]))
						self.query("update users set pass = ? where name = ? and email = ?", self.encode(newpw), arg[0], arg[1])
						self.mail(data["email"], "From: %s <%s>\nTo: %s <%s>\nSubject: Password reset\nThis is an automated message, do not respond to this email!\n\nAccount: %s\nPassword: %s" % (self.services_description, self.email, data["name"], data["email"], data["name"], newpw))
						self.msg(uid, "I've sent an email with your lost password to %s." % data["email"])
					else:
						self.msg(uid, "Your account have been banned from " + self.services_description + ". Reason: " + data["suspended"])
						
				if not entry:
					self.msg(uid, "Can't find user " + arg[0] + " with email " + arg[1] + ".")
			else:
				self.msg(uid, "Syntax: RESETPASS <account> <email>")
		else:
			self.msg(uid, "RESETPASS is not available once you have authed.")
