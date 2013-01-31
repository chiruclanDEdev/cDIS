from chiruserv import CServMod
from socket import getfqdn, getaddrinfo

class cmd_hostinfo(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "HOSTINFO"
	HELP = "Get information about a domain or IP"
	NEED_OPER = 1
	
	def onCommand(self, uid, args):
		if len(args.split()) == 1:
			self.msg(uid, "-=- Get Domain/IP information -=-")
			self.msg(uid)
			msg(uid, "Host: " + getfqdn(args))
			
			ip = "0.0.0.0"
			
			for data in getaddrinfo(args, None):
				if ip != data[4][0]:
					ip = data[4][0]
					
					if ip.find(":") != -1:
						self.msg(uid, "IPv6: " + ip)
					else:
						self.msg(uid, "IP: " + ip)
						
			self.msg(uid)
			self.msg(uid, "-=- End of Domain/IP information -=-")
		else:
			self.msg(uid, "Syntax: " + COMMAND + " <hostname/ip>")