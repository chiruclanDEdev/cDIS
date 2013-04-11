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

class cmd_4_userflags(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "USERFLAGS"
	HELP = "Changes and shows the userflags of other users"
	NEED_OPER = 1
	BOT_ID = '4'

	def onCommand(self, uid, args):
		mode = list()
		desc = list()
		mode.append("n")
		desc.append("Q will answer with notices, instead of privmsgs.")
		mode.append("a")
		desc.append("Autojoin all channels where you have chanflag +v or higher.")
		mode.append("x")
		desc.append("Cloak your hostname.")
		arg = args.split()
		
		if len(arg) == 1:
			self.msg(uid, "Current user flags: +"+self.userflags(self.uid(arg[0])))
		elif len(arg) == 2:
			if arg[0] == "?":
				i = 0
				
				while i != len(mode):
					self.msg(uid, "+" + mode[i]+" = "+desc[i])
					i += 1
			else:
				userflags = self.regexflag("+" + self.userflags(self.uid(arg[0])), arg[1])
				flags = ''.join([char for char in userflags if char in ''.join(mode)])
				self.query("update users set flags = ? where name = ?", flags, self.auth(self.uid(arg[0])))
				self.msg(uid, "Done. Current user flags for " + arg[0] + ": +" + userflags)
				if arg[1].find("x") != -1:
					for target in self.sid(arg[0]):
						self.vhost(target)
		else:
			self.msg(uid, "Syntax: SAUSERFLAGS <user> [<flags>]")