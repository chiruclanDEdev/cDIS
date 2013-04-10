from cDIS import cDISModule

class mod_3_join(cDISModule):
	MODULE_CLASS = "JOIN"
	BOT_ID = '3'
	
	def onData(self, data):
		juid = data.split()[0][1:]
		jchan = data.split()[2][1:]
		self.query("insert into chanlist value (?, ?, '')", juid, jchan)
		
		if self.suspended(jchan):
			self.kick(jchan, juid, "Suspended: "+self.suspended(jchan))
			
		if self.chanexist(jchan):
			self.enforcebans(jchan)
			
		if self.chanflag("l", jchan):
			self.showlog(juid, jchan)
			self.log(juid, "join", jchan)
			
		self.flag(juid, jchan)
		
		if self.chanflag("v", jchan):
			self.mode(jchan, "+v %s" % juid)
				
		for welcome in self.query("select name,welcome from channelinfo where name = ?", jchan):
			if self.chanflag("w", jchan):
				self.msg(juid, "[{0}] {1}".format(welcome["name"], welcome["welcome"]))
				
		if self.isoper(juid) and self.chanexist(jchan):
			self.send(":%s NOTICE %s :Operator %s has joined" % (self.services_id, jchan, self.nick(juid)))