from chiruserv import CSModules, config

class accban(CSModules):
	HELP = "Bans an account from " + config.get("SERVICES", "description")
	NEED_OPER = 1

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 0:
			self.msg(uid, "Account                 Reason")
			
			for data in self.query("select * from users where suspended != '0'"):
				self.msg(uid, "  {0} {1} {2}".format(data["name"], " "*int(20-len(data["name"])), data["suspended"]))
				
			self.msg(uid, "End of list.")
		elif len(arg) == 1:
			entry = False
			
			if arg[0][0] == "?":
				if self.user(arg[0][1:]):
					self.msg(uid, "Suspend status of account " + arg[0][1:] + ": " + str(self.banned(arg[0][1:])))
				else:
					self.msg(uid, "Can't find user " + arg[0][1:])
			else:
				if self.user(arg[0]):
					self.query("update users set suspended = '0' where name = ?", arg[0])
					self.msg(uid, "Done.")
				else:
					self.msg(uid, "Can't find user " + arg[0])
		elif len(arg) > 1:
			if self.user(arg[0]):
				self.query("update users set suspended = ? where name = ?", ' '.join(arg[1:]), arg[0])
				self.msg(uid, "Done.")
			else:
				self.msg(uid, "Can't find user " + arg[0])