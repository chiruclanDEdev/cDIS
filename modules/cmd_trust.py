from chiruserv import CServMod

class cmd_trust(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "TRUST"
	HELP = "Manage IP trusts for your network"
	NEED_OPER = 1

	def onCommand(self, source, args):
		arg = args.split()
		if len(arg) > 1:
			trip = arg[1]
		
		if len(arg) == 1 and arg[0] == "list":
			for trust in self.query("select * from trust order by id"):
				self.msg(source, "IP: {0} {2} Limit: {1}".format(trust["address"], trust["limit"], ' '*int(23-len(trust["address"]))))
		elif len(arg) == 2 and arg[0] == "remove":
			entry = False
			
			for trust in self.query("select * from trust where address = ?", trip):
				entry = True
				self.query("delete from trust where address = ?", trust["address"])
				
			if entry:
				self.msg(source, "Trust for {0} has been deleted.".format(arg[1]))
				conns = 0
				nicks = list()
				
				for online in self.query("select uid from online where address = ?", trip):
					nicks.append(online["uid"])
					conns += 1
					
				for nick in nicks:
					self.msg(self.uid(nick), "Your trust has been set to '3'.")
					
				if conns > 3 and arg[1] != "0.0.0.0":
					for nick in nicks:
						self.send(":{0} KILL {1} :G-lined".format(self.bot, nick))
						
					self.send(":{0} GLINE *@{1} 1800 :Connection limit (3) reached".format(self.bot, arg[1]))
				elif conns == 3 and arg[1] != "0.0.0.0":
					for nick in nicks:
						self.msg(nick, "Your IP is scratching the connection limit. If you need more connections please request a trust and give us a reason on #help.")
			else:
				self.msg(source, "Trust for {0} does not exist.".format(arg[1]))
		elif len(arg) == 3 and arg[0] == "set":
			entry = False
			
			for trust in self.query("select * from trust where address = ?", trip):
				entry = True
				
			if entry:
				limit = filter(lambda x: x.isdigit(), arg[2])
				
				if limit != "":
					self.query("update trust set `limit` = ? where address = ?", limit, trip)
					self.msg(source, "Trust for {0} has been set to {1}.".format(arg[1], limit))
					conns = 0
					nicks = list()
					invalid = False
					
					for online in self.query("select nick from online where address = ?", trip):
						nicks.append(online["nick"])
						conns += 1
						
					for nick in nicks:
						self.msg(self.uid(nick), "Your trust has been set to '{0}'.".format(limit))
						
					if conns > int(limit) and arg[1] != "0.0.0.0" and int(limit) != 0:
						for nick in nicks:
							self.send(":{0} KILL {1} :G-lined".format(self.bot, nick))
							
						self.send(":{0} GLINE *@{1} 1800 :Connection limit ({2}) reached".format(self.bot, arg[1], limit))
					elif conns == int(limit) and arg[1] != "0.0.0.0" and int(limit) != 0:
						for nick in nicks:
							self.msg(nick, "Your IP is scratching the connection limit. If you need more connections please request a trust and give us a reason on #help.")
							
					for username in self.query("select username from online where address = ?", trip):
						if username["username"].startswith("~"):
							for nick in nicks:
								self.send(":{0} KILL {1} :G-lined".format(self.bot, nick))
								
							self.send(":{0} GLINE *@{1} 1800 :You ignored the trust rules. Run an identd before you connect again.".format(self.bot, arg[1]))
				else:
					self.msg(source, "Invalid limit")
			else:
				limit = filter(lambda x: x.isdigit(), arg[2])
				
				if limit != "":
					self.query("insert into trust (`address`, `limit`) values (?, ?)", limit, trip)
					self.msg(source, "Trust for {0} has been set to {1}.".format(arg[1], limit))
					conns = 0
					nicks = list()
					
					for online in self.query("select nick from online where address = ?", trip):
						nicks.append(online["nick"])
						conns += 1
						
					for nick in nicks:
						self.msg(self.uid(nick), "Your trust has been set to '{0}'.".format(limit))
						
					if conns > int(limit) and arg[1] != "0.0.0.0" and int(limit) != 0:
						for nick in nicks:
							self.send(":{0} KILL {1} :G-lined".format(self.bot, nick))
							
						self.send(":{0} GLINE *@{1} 1800 :Connection limit ({2}) reached".format(self.bot, arg[1], limit))
					elif conns == int(limit) and arg[1] != "0.0.0.0" and int(limit) != 0:
						for nick in nicks:
							self.msg(nick, "Your IP is scratching the connection limit. If you need more connections please request a trust and give us a reason on #help.")
							
					for username in self.query("select username from online where address = ?", trip):
						if username["username"].startswith("~"):
							for nick in nicks:
								self.send(":{0} KILL {1} :G-lined".format(self.bot, nick))
								
							self.send(":{0} GLINE *@{1} 1800 :You ignored the trust rules. Run an identd before you connect again.".format(self.bot, arg[1]))
				else:
					self.msg(source, "Invalid limit")
		else:
			self.msg(source, "Syntax: TRUST <list/set/remove> [<address> [<limit>]]")