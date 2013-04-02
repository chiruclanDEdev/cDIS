from cDIS import cDISModule
from socket import getfqdn, getaddrinfo

class 4_cmd_hostinfo(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "HOSTINFO"
	HELP = "Get information about a domain or IP"
	NEED_OPER = 1
	BOT_ID = '4'
	
	def onCommand(self, uid, args):
		if len(args.split()) == 1:
			self.msg(uid, "-=- Get Domain/IP information -=-")
			self.msg(uid)
			try:
				self.msg(uid, "Host: " + getfqdn(args))
				
				ip = "0.0.0.0"
				
				for data in getaddrinfo(args, None):
					if ip != data[4][0]:
						ip = data[4][0]
						
						if ip.find(":") != -1:
							self.msg(uid, "IPv6: " + ip)
						else:
							self.msg(uid, "IP: " + ip)
			except Exception:
				self.msg(uid, "Seems like something has gone wrong.")
				
			self.msg(uid)
			self.msg(uid, "-=- End of Domain/IP information -=-")
		else:
			self.msg(uid, "Syntax: HOSTINFO <hostname/ip>")