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
from time import time

class cmd_4_resetpass(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "RESETPASS"
	HELP = "Reset your lost password"
	NEED_OPER = 1
	BOT_ID = '4'

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 1:
			entry = False
			
			for data in self.query("select name,pass,email,suspended from users where name = ?", arg[0]):
				entry = True
				
				if data["suspended"] == "0":
					newpw = str(hash(str(time()) + data["name"] + data["pass"] + data["email"]))
					self.query("update users set pass = ? where name = ? and email = ?", self.encode(newpw), data["name"], data["email"])
					self.msg(uid, "The new password of the user {0} is {1}. He/She should change it as soon as possible!".format(data["name"], newpw))
				else:
					self.msg(uid, "The account have been banned from " + self.services_description + ". Reason: " + data["suspended"])
					
			if not entry:
				self.msg(uid, "Can't find user " + arg[0] + ".")
		else:
			self.msg(uid, "Syntax: RESETPASS <account>")
