from chiruserv import CServMod

class fmode(CServMod):
	MODULE_CLASS = "FMODE"
	
	def onData(self, data):
		if self.chanflag("l", data.split()[2]) and len(data.split()) > 4:
			self.log(data.split()[0][1:], "mode", data.split()[2], ' '.join(data.split()[4:]))
			
		if self.chanflag("m", data.split()[2]) and len(data.split()) == 5:
			if data.split()[2].startswith("#"):
				for channel in self.query("select name,modes from channelinfo where name = ?", data.split()[2]):
					self.mode(channel["name"], channel["modes"])
					
		if len(data.split()) > 5:
			if self.chanexist(data.split()[2]):
				splitted = data.split()[4]
				
				if splitted.find("+") != -1:
					splitted = splitted.split("+")[1]
					
				if splitted.find("-") != -1:
					splitted = splitted.split("-")[0]
					
				flag = self.getflag(data.split()[0][1:], data.split()[2])
				
				if flag == "h" or flag == "o" or flag == "a" or flag == self.bot_nick or flag == "n":
					if splitted.find("b") != -1:
						self.checkbans(data.split()[2], ' '.join(data.split()[5:]))
						
						for ban in data.split()[5:]:
							if fnmatch.fnmatch(ban, "*!*@*"):
								entry = False
								
								for sql in self.query("select ban from banlist where ban = ? and channel = ?", ban, data.split()[2]):
									entry = True
									
								if not entry and ban != "*!*@*":
									self.query("insert into banlist (`channel`, `ban`) values (?, ?)", data.split()[2], ban)
									self.msg(data.split()[0][1:], "Done.")
								elif ban == "*!*@*":
									self.msg(data.split()[2], "ACTION is angry about %s, because he tried to set a *!*@* ban." % self.nick(data.split()[0][1:]), True)
				else:
					self.mode(data.split()[2], "-{0} {1}".format("b"*len(data.split()[5:]), ' '.join(data.split()[5:])))
					
				splitted = data.split()[4]
				
				if splitted.find("-") != -1:
					splitted = splitted.split("-")[1]
					
					if splitted.find("+") != -1:
						splitted = splitted.split("+")[0]
						
					flag = self.getflag(data.split()[0][1:], data.split()[2])
					
					if flag == "h" or flag == "o" or flag == "a" or flag == self.bot_nick or flag == "n":
						if splitted.find("b") != -1:
							for ban in data.split()[5:]:
								if fnmatch.fnmatch(ban, "*!*@*"):
									entry = False
									
									for sql in self.query("select ban from banlist where channel = ? and ban = ?", data.split()[2], ban):
										entry = True
										
									if entry:
										self.query("delete from banlist where channel = ? and ban = ?", data.split()[2], ban)
										self.msg(data.split()[0][1:], "Done.")
					else:
						self.mode(data.split()[2], "+{0} {1}".format("b"*len(data.split()[5:]), ' '.join(data.split()[5:])))
						
			if self.chanflag("b", data.split()[2]):
				mchan = data.split()[2]
				splitted = data.split()[4]
				musers = data.split()[5:]
				
				if splitted.find("+") != -1:
					splitted = splitted.split("+")[1]
					
					if splitted.find("-") != -1:
						splitted = splitted.split("-")[0]
						
					if splitted.find("v") != -1:
						for user in musers:
							flag = self.getflag(self.uid(user), mchan)
							
							if not self.chanflag("v", mchan) and flag != "v" and flag != "h" and flag != "o" and flag != "a" and flag != "q" and flag != "n" and self.uid(user) != self.bot:
								self.mode(mchan, "-v "+user)
								
					if splitted.find("h") != -1:
						for user in musers:
							flag = self.getflag(self.uid(user), mchan)
							
							if flag != "h" and flag != "o" and flag != "a" and flag != "q" and flag != "n" and self.uid(user) != self.bot:
								self.mode(mchan, "-h "+user)
								
					if splitted.find("o") != -1:
						for user in musers:
							flag = self.getflag(self.uid(user), mchan)
							
							if flag != "o" and flag != "a" and flag != "q" and flag != "n" and self.uid(user) != self.bot:
								self.mode(mchan, "-o "+user)
								
					if splitted.find("a") != -1:
						for user in musers:
							flag = self.getflag(self.uid(user), mchan)
							
							if flag != "a" and flag != self.bot_nick and flag != "n" and self.uid(user) != self.bot:
								self.mode(mchan, "-a "+user)
								
							if flag != "o":
								self.mode(mchan, "-o "+user)
								
					if splitted.find(self.bot_nick) != -1:
						for user in musers:
							flag = self.getflag(self.uid(user), mchan)
							
							if flag != "q" and flag != "n" and self.uid(user) != self.bot:
								self.mode(mchan, "-q "+user)
								
							if flag != "o":
								self.mode(mchan, "-o "+user)
								
			if self.chanflag("p", data.split()[2]):
				for user in data.split()[5:]:
					fm_chan = data.split()[2]
					
					for flag in self.query("select flag from channels where channel = ? and user = ?", data.split()[2], self.auth(user)):
						if flag["flag"] == "n" or flag["flag"] == "q":
							self.mode(fm_chan, "+qo {0} {0}".format(user))
						elif flag["flag"] == "a":
							self.mode(fm_chan, "+ao {0} {0}".format(user))
						elif flag["flag"] == "o":
							self.mode(fm_chan, "+o {0}".format(user))
						elif flag["flag"] == "h":
							self.mode(fm_chan, "+h {0}".format(user))
						elif flag["flag"] == "v":
							self.mode(fm_chan, "+v {0}".format(user))
						elif flag["flag"] == "b":
							self.kick(fm_chan, user, "Banned.")