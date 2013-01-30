from chiruserv import CSModules
from time import time

class saresetpass(CSModules):
	HELP = "Reset your lost password"
	NEED_OPER = 1

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 1:
			entry = False
			
			for data in self.query("select name,pass,email,suspended from users where name = ?", arg[0]):
				entry = True
				
				if data["suspended"] == "0":
					newpw = str(hash(str(time()) + data["name"] + data["pass"] + data["email"]))
					self.query("update users set pass = ? where name = ? and email = ?", self.encode(newpw), data["name"], data["email"])
					self.msg(uid, "The new password of the user {0} is {1}. He/She should change it as soon as possible!".format(data["name"], newpw))
				else:
					self.msg(uid, "The account have been banned from " + self.services_description + ". Reason: " + data["suspended"])
					
			if not entry:
				self.msg(uid, "Can't find user " + arg[0] + ".")
		else:
			self.msg(uid, "Syntax: RESETPASS <account>")
