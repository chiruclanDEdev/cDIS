from chiruserv import CServMod
from socket import getfqdn, getaddrinfo

class cmd_hostinfo(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "HOSTINFO"
	HELP = "Get information about a domain or IP"
	NEED_OPER = 1
	
	def onCommand(self, uid, args):
		msg(nick, "-=- Get Domain/IP information -=-")
		msg(nick)
		msg(nick, "Host: " + getfqdn(args))
		
		ip = "0.0.0.0"
		
		for data in getaddrinfo(args, None):
			if ip != data[4][0]:
				ip = data[4][0]
				
				if ip.find(":") != -1:
					msg(nick, "IPv6: " + ip)
				else:
					msg(nick, "IP: " + ip)
					
		msg(nick)
		msg(nick, "-=- End of Domain/IP information -=-")