# chiruclan.de IRC services
# Copyright (C) 2012-2013  Chiruclan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from cDIS import cDISModule
from socket import getfqdn, getaddrinfo

class cmd_4_hostinfo(cDISModule):
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