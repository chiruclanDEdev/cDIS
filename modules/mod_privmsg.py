from chiruserv import CServMod
import __builtin__

class mod_privmsg(CServMod):
	MODULE_CLASS = "PRIVMSG"
	
	def onData(self, data):
		if data.split()[2].startswith("#") and self.chanflag("l", data.split()[2]):
			self.log(data.split()[0][1:], "privmsg", data.split()[2], ' '.join(data.split()[3:]))
					
		if self.chanexist(data.split()[2]):
			puid = data.split()[0][1:]
			pchan = data.split()[2]
			
			if self.chanflag("s", pchan):
				messages = 10
				seconds = [6, 5]
				
				for dump in self.query("select spamscan from channelinfo where name = ?", pchan):
					messages = int(dump["spamscan"].split(":")[0])
					seconds = [int(dump["spamscan"].split(":")[1]) + 1, int(dump["spamscan"].split(":")[1])]
					
				if spamscan.has_key((pchan, puid)):
					num = spamscan[pchan,puid][0] + 1
					spamscan[pchan,puid] = [num, spamscan[pchan,puid][1]]
					timer = int(time.time()) - spamscan[pchan,puid][1]
					
					if spamscan[pchan,puid][0] == messages and timer < seconds[0]:
						if self.isoper(puid):
							self.msg(puid, "WARNING: You are flooding {0}. Please stop that, but I won't kill you because you're an IRC Operator.".format(pchan))
						else:
							self.kill(puid)
							
						del spamscan[pchan,puid]
					elif timer > seconds[1]:
						spamscan[pchan,puid] = [1, int(time.time())]
				else:
					spamscan[pchan,puid] = [1, int(time.time())]
					
		__builtin__.spamscan = spamscan