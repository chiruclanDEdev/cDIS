from chiruserv import CServMod

class mod_uid(CServMod):
	MODULE_CLASS = "UID"
	
	def onData(self, data):
				self.query("delete from temp_nick where nick = ?", data.split()[2])
				self.query("delete from gateway where uid = ?", data.split()[2])
				self.query("delete from online where uid = ?", data.split()[2])
				self.query("delete from online where nick = ?", data.split()[4])
				self.query("insert into online values (?, ?, ?, ?, ?)", data.split()[2], data.split()[4], data.split()[8], data.split()[5], data.split()[7])
				conns = 0
				nicks = list()
				
				for connection in self.query("select nick from online where address = ?", data.split()[8]):
					nicks.append(connection["nick"])
					conns += 1
					
				limit = 3
				
				for trust in self.query("select `limit` from trust where address = ?", data.split()[8]):
					limit = int(trust["limit"])
					
					if data.split()[7].startswith("~"):
						for nick in nicks:
							self.send(":{0} KILL {1} :G-lined".format(self.bot, nick))
							
						self.send(":{0} GLINE *@{1} 1800 :You ignored the trust rules. Run an identd before you connect again.".format(self.bot, data.split()[8]))
						
				if conns > limit and data.split()[8] != "0.0.0.0" and limit != 0:
					for nick in nicks:
						self.send(":{0} KILL {1} :G-lined".format(self.bot, nick))
						
					self.send(":{0} GLINE *@{1} 1800 :Connection limit ({2}) reached".format(self.bot, data.split()[8], limit))
				elif conns == limit and data.split()[8] != "0.0.0.0":
					for nick in nicks:
						self.msg(nick, "Your IP is scratching the connection limit. If you need more connections please request a trust and give us a reason on #help.")
						
				for ip in self.query("select channel from ipchan where ip = ?", data.split()[8]):
					self.send(":%s SVSJOIN %s %s" % (self.bot, data.split()[2], ip["channel"]))
					
				if data.split()[10].find("B") != -1:
					crypthost = self.encode_md5(data.split()[2] + ":" + self.nick(data.split()[2]) + "!" + self.userhost(data.split()[2]))
					self.send(":%s CHGHOST %s %s.gateway.%s" % (self.services_id, data.split()[2], crypthost, '.'.join(self.services_name.split(".")[-2:])))
					self.query("insert into gateway values (?)", data.split()[2])