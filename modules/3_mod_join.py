from cDIS import cDISModule

class 3_mod_join(cDISModule):
	MODULE_CLASS = "JOIN"
	BOT_ID = '3'
	
	def onData(self, data):
		juid = data.split()[0][1:]
		jchan = data.split()[2][1:]
		self.query("insert into chanlist value (?, ?)", juid, jchan)
		
		if self.suspended(jchan):
			self.kick(jchan, juid, "Suspended: "+self.suspended(jchan))
			
		if self.chanexist(jchan):
			self.enforcebans(jchan)
			
		if self.chanflag("l", jchan):
			self.showlog(juid, jchan)
			self.log(juid, "join", jchan)
			
		fjoin_user = self.auth(juid)
		hasflag = False
		
		for flag in self.query("select flag from channels where channel = ? and user = ?", jchan, fjoin_user):
			if flag["flag"] == "n" or flag["flag"] == "q":
				self.mode(jchan, "+qo " + juid + " " + juid)
				hasflag = True
			elif flag["flag"] == "a":
				self.mode(jchan, "+ao " + juid + " " + juid)
				hasflag = True
			elif flag["flag"] == "o":
				self.mode(jchan, "+o " + juid)
				hasflag = True
			elif flag["flag"] == "h":
				self.mode(jchan, "+h " + juid)
				hasflag = True
			elif flag["flag"] == "v":
				self.mode(jchan, "+v " + juid)
				hasflag = True
			elif flag["flag"] == "b":
				self.kick(jchan, juid, "Banned.")
				hasflag = True
				
		if not hasflag:
			if self.chanflag("v", jchan):
				self.mode(jchan, "+v %s" % juid)
				
		for welcome in self.query("select name,welcome from channelinfo where name = ?", jchan):
			if self.chanflag("w", jchan):
				self.msg(juid, "[{0}] {1}".format(welcome["name"], welcome["welcome"]))
				
		if self.isoper(juid) and self.chanexist(jchan):
			self.send(":%s NOTICE %s :Operator %s has joined" % (self.services_id, jchan, self.nick(juid)))