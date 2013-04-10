from cDIS import cDISModule

class mod_3_fjoin(cDISModule):
	MODULE_CLASS = "FJOIN"
	BOT_ID = '3'
	
	def onData(self, data):
		fjoin_chan = data.split()[2]
			
		for pdata in data.split()[5:]:
			pflag = pdata.split(",")[0]
			pnick = pdata.split(",")[1]
				
			self.query("insert into chanlist (uid, channel, flag) values (?,?,?)", pnick, fjoin_chan, pflag)
			
			if self.suspended(fjoin_chan):
				if not self.isoper(pnick):
					self.kick(fjoin_chan, pnick, "Suspended: "+self.suspended(fjoin_chan))
				else:
					self.msg(fjoin_chan, "This channel is suspended: "+self.suspended(fjoin_chan))

			if self.chanexist(fjoin_chan):
				self.enforcebans(fjoin_chan)
			
			fjoin_user = self.auth(pnick)
			hasflag = False
			
			for flag in self.query("select flag from channels where channel = ? and user = ?", fjoin_chan, fjoin_user):
				if flag["flag"] == "n" or flag["flag"] == "q":
					self.mode(fjoin_chan, "+qo " + pnick + " " + pnick)
					hasflag = True
				elif flag["flag"] == "a":
					self.mode(fjoin_chan, "+ao " + pnick + " " + pnick)
					hasflag = True
				elif flag["flag"] == "o":
					self.mode(fjoin_chan, "+o " + pnick)
					hasflag = True
				elif flag["flag"] == "h":
					self.mode(fjoin_chan, "+h " + pnick)
					hasflag = True
				elif flag["flag"] == "v":
					self.mode(fjoin_chan, "+v " + pnick)
					hasflag = True
				elif flag["flag"] == "b":
					self.kick(fjoin_chan, pnick, "Banned.")
					hasflag = True
					
				self.setuserchanflag(fjoin_chan, pnick, flag["flag"].replace('n', 'q'))
					
			if not hasflag:
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