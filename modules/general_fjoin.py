from chiruserv import Module

class general_fjoin(Module):
	MODULE_CLASS = "FJOIN"
	
	def onData(self, data):
		fjoin_chan = data.split()[2]
		fjoin_nick = data.split()[5][1:]
		
		if fjoin_nick.find(",") != -1:
			fjoin_nick = fjoin_nick.split(",")[1]
			
		for pnick in data.split()[5:]:
			if pnick.find(",") != -1:
				pnick = pnick.split(",")[1]
				
			self.query("insert into chanlist value (?,?)", pnick, fjoin_chan)
			
			if self.suspended(fjoin_chan):
				if not self.isoper(pnick):
					self.kick(fjoin_chan, pnick, "Suspended: "+self.suspended(fjoin_chan))
				else:
					self.msg(fjoin_chan, "This channel is suspended: "+self.suspended(fjoin_chan))
					
		if self.chanexist(fjoin_chan):
			self.enforcebans(fjoin_chan)
			
		if self.chanflag("l", fjoin_chan):
			self.showlog(fjoin_nick, fjoin_chan)
			self.log(fjoin_nick, "join", fjoin_chan)
			
		fjoin_user = self.auth(fjoin_nick)
		hasflag = False
		
		for flag in self.query("select flag from channels where channel = ? and user = ?", fjoin_chan, fjoin_user):
			if flag["flag"] == "n" or flag["flag"] == "q":
				self.mode(fjoin_chan, "+qo " + fjoin_nick + " " + fjoin_nick)
				hasflag = True
			elif flag["flag"] == "a":
				self.mode(fjoin_chan, "+ao " + fjoin_nick + " " + fjoin_nick)
				hasflag = True
			elif flag["flag"] == "o":
				self.mode(fjoin_chan, "+o " + fjoin_nick)
				hasflag = True
			elif flag["flag"] == "h":
				self.mode(fjoin_chan, "+h " + fjoin_nick)
				hasflag = True
			elif flag["flag"] == "v":
				self.mode(fjoin_chan, "+v " + fjoin_nick)
				hasflag = True
			elif flag["flag"] == "b":
				self.kick(fjoin_chan, fjoin_nick, "Banned.")
				hasflag = True
				
		if not hasflag:
			if self.chanflag("v", fjoin_chan):
				self.mode(fjoin_chan, "+v %s" % fjoin_nick)
				
		for welcome in self.query("select name,welcome from channelinfo where name = ?", fjoin_chan):
			if self.chanflag("w", fjoin_chan):
				self.msg(fjoin_nick, "[{0}] {1}".format(welcome["name"], welcome["welcome"].replace(":topic:", self.gettopic(fjoin_chan))))
				
		if self.isoper(fjoin_nick) and self.chanexist(fjoin_chan):
			self.send(":%s NOTICE %s :Operator %s has joined" % (self.services_id, fjoin_chan, self.nick(fjoin_nick)))