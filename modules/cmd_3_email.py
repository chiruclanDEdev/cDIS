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

class cmd_3_email(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "EMAIL"
	HELP = "Changes your account email"
	NEED_AUTH = 1
	BOT_ID = '3'

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].find("@") != -1:
				if len(arg[0].split("@")[0]) != 0:
					if arg[0].split("@")[1].find(".") != -1:
						if arg[0].split("@")[1][-1] != "." and arg[0].split("@")[1][-2] != "." and arg[0].split("@")[1][0] != ".":
							entry = False
							
							for data in self.query("select * from users where email = ?", arg[0]):
								entry = True
								
							if not entry:
								self.query("update users set email = ? where name = ?", arg[0], self.auth(uid))
								self.mail(arg[0], "From: {server} <{servermail}>\nTo: {user} <{usermail}>\nSubject: Email verification\nYour Email address has been changed to {usermail} successfully.".format(server=self.services_description, servermail=self.email, user=self.auth(uid), usermail=arg[0]))
								self.msg(uid, "Done.")
							else:
								self.msg(uid, "Email address already in use.")
						else:
							self.msg(uid, "Invalid email: "+arg[0])
					else:
						self.msg(uid, "Invalid email: "+arg[0])
				else:
					self.msg(uid, "Invalid email: "+arg[0])
			else:
				self.msg(uid, "Invalid email: "+arg[0])
		else:
			self.msg(uid, "Syntax: EMAIL <email>")
