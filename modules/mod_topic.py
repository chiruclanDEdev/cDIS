from cDIS import cDISModule

class mod_topic(cDISModule):
	MODULE_CLASS = "TOPIC"
	
	def onData(self, data):
		if len(data.split()) > 1:
			if self.chanflag("l", data.split()[2]):
				self.log(data.split()[0][1:], "topic", data.split()[2], ' '.join(data.split()[3:]))
				
			if self.chanflag("t", data.split()[2]):
				for channel in self.query("select topic from channelinfo where name = ?", data.split()[2]):
					self.send(":{0} TOPIC {1} :{2}".format(self.bot, data.split()[2], channel["topic"]))
					
					if self.chanflag("l", data.split()[2]):
						self.log(self.bot_nick, "topic", data.split()[2], ":"+channel["topic"])