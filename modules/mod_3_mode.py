from cDIS import cDISModule

class mod_3_mode(cDISModule):
	MODULE_CLASS = "MODE"
	BOT_ID = '3'
	
	def onData(self, data):
		smodes = data.split()[3]
		
		if smodes.find("+") != -1:
			smodes = smodes.split("+")[1]
			
			if smodes.find("-") != -1:
				smodes = smodes.split("-")[0]
				
			if smodes.find("B") != -1:
				crypthost = self.encode_md5(data.split()[0][1:] + ":" + self.nick(data.split()[0][1:]) + "!" + self.userhost(data.split()[0][1:]))
				self.send(":%s CHGHOST %s %s.gateway.%s" % (self.services_id, data.split()[0][1:], crypthost, '.'.join(self.services_name.split(".")[-2:])))
				self.query("insert into gateway values (?)", data.split()[0][1:])
				
		smodes = data.split()[3]
		
		if smodes.find("-") != -1:
			smodes = smodes.split("-")[1]
			
			if smodes.find("+") != -1:
				smodes = smodes.split("+")[0]
				
			if smodes.find("B") != -1:
				self.send(":%s CHGHOST %s %s" % (self.bot, data.split()[0][1:], self.gethost(data.split()[0][1:])))
				self.query("delete from gateway where uid = ?", data.split()[0][1:])