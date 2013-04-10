from cDIS import cDISModule

class mod_3_fjoin(cDISModule):
	MODULE_CLASS = "FJOIN"
	BOT_ID = '3'
	
	def onData(self, data):
		fjoin_chan = data.split()[2]
		
		for pdata in data.split()[5:]:
			pflag = pdata.split(",")[0]
			pnick = pdata.split(",")[1]
			
			self.query('INSERT INTO `chanlist` (`uid`, `channel`, `flag`) VALUES (?, ?, ?)', pnick, fjoin_chan, pflag)
			
			if self.suspended(fjoin_chan):
				if not self.isoper(pnick):
					self.kick(fjoin_chan, pnick, "Suspended: "+self.suspended(fjoin_chan))
				else:
					self.msg(fjoin_chan, "This channel is suspended: "+self.suspended(fjoin_chan))

			if self.chanexist(fjoin_chan):
				self.enforcebans(fjoin_chan)
			
			self.flag(pnick, fjoin_chan)
			
			if self.chanflag("v", fjoin_chan):
				self.mode(fjoin_chan, "+v %s" % pnick)
					
			for welcome in self.query("select name,welcome from channelinfo where name = ?", fjoin_chan):
				if self.chanflag("w", fjoin_chan):
					self.msg(pnick, "[{0}] {1}".format(welcome["name"], welcome["welcome"].replace(":topic:", self.gettopic(fjoin_chan))))
					
			if self.isoper(pnick) and self.chanexist(fjoin_chan):
				self.send(":%s NOTICE %s :Operator %s has joined" % (self.services_id, fjoin_chan, self.nick(pnick)))
				
			if self.chanflag("l", fjoin_chan):
				self.showlog(pnick, fjoin_chan)
				self.log(pnick, "join", fjoin_chan)