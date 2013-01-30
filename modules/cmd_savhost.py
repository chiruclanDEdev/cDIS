from chiruserv import CServMod

class cmd_savhost(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "SAVHOST"
	HELP = "Manages vhosts of the users"
	NEED_OPER = 1

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 0:
			self.msg(source, "Account                   vHost")
			
			for data in self.query("select user,vhost from vhosts where active = '0'"):
				self.msg(source, "  %s %s %s" % (str(data["user"]), " "*int(20-len(data["user"])), str(data["vhost"])))
				
			self.msg(source, "End of list.")
		elif len(arg) == 1:
			if arg[0] == "?list":
				self.msg(source, "Account                 vHost")
				
				for data in self.query("select user,vhost from vhosts where active = '1'"):
					self.msg(source, "  {0} {1} {2}".format(data["user"], " "*int(20-len(data["user"])), data["vhost"]))
					
				self.msg(source, "End of list.")
			else:
				for data in self.query("select user,vhost from vhosts where active = '0' and user = ?", arg[0]):
					self.query("update vhosts set active = '1' where user = ?", str(data["user"]))
					self.query("insert into memo (`user`, `source`, `message`) values (?, ?, ?)", data["user"], self.bot_nick, "Your vHost {0} has been activated.".format(data["vhost"]))
					
					for uid in self.sid(data["user"]):
						self.vhost(uid)
						
					self.memo(data["user"])
					self.msg(source, "Done.")
		elif len(arg) > 1:
			if arg[0] == "?set":
				if self.user(arg[1]):
					entry = False
					
					for data in self.query("select user,vhost from vhosts where vhost = ?", arg[2]):
						user = data["user"]
						vhost = data["vhost"]
						entry = True
						
					if not entry:
						self.query("delete from vhosts where user = ?", arg[1])
						self.query("insert into vhosts values (?, ?, '1')", self.user(arg[1]), arg[2])
						self.query("insert into memo (`user`, `source`, `message`) values (?, ?, ?)", self.user(arg[1]), self.bot_nick, "{0} has been set as your vHost".format(arg[2]))
						
						for uid in self.sid(arg[1]):
							self.vhost(uid)
							
						self.memo(arg[1])
						self.msg(source, "Done.")
					else:
						self.msg(source, "User %s is alreading using this vHost (%s)." % (user, vhost))
				else:
					self.msg(source, "Can't find user "+arg[1]+".")
			elif arg[0] == "?unset":
				if self.user(arg[1]):
					vhost = self.getvhost(arg[1])
					self.query("delete from vhosts where user = ?", arg[1])
					self.query("insert into memo (`user`, `source`, `message`) values (?, ?, ?)", self.user(arg[1]), self.bot_nick, "Your vHost {0} has been deleted.".format(vhost))
					
					for uid in self.sid(arg[1]):
						self.vhost(uid)
						
					self.memo(arg[1])
					self.msg(source, "Done.")
				else:
					self.msg(source, "Can't find user " + arg[1] + ".")
			else:
				for data in self.query("select * from vhosts where active = '0' and user = ?", arg[0]):
					self.query("delete from vhosts where user = ?", str(data["user"]))
					self.msg(source, "vHost for user %s has been rejected" % str(data["user"]))
					self.query("insert into memo (`user`, `source`, `message`) values (?, ?, ?)", data["user"], self.bot_nick, data["vhost"], "Your vHost %s has been rejected. Reason: " + ' '.join(arg[1:]))
					self.memo(data[0])
		else:
			self.msg(source, "Syntax: SAVHOST [?list] [[?set] <user> [<reject-reason>]]")
