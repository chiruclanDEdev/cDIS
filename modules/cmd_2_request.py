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

class cmd_2_request(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "REQUEST"
	HELP = "Requests the channel service for your channel"
	NEED_AUTH = 1
	BOT_ID = '2'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if not self.chanexist(arg[0]):
					if not self.suspended(arg[0]):
						cucflag = self.currentuserchanflag(arg[0], source)
						if cucflag == "q" or cucflag == "a" or cucflag == "o":
							if self.channelusercount(arg[0]) >= 10:
								self.query("insert into channelinfo values (?, '', '', '', '', '10:5', '!')", arg[0])
								self.query("insert into channels values (?, ?, 'n')", arg[0], self.auth(source))
								self.join(arg[0])
								self.mode(arg[0], "+qo {0} {0}".format(source))
								self.msg(source, "Channel %s has been registered for you" % arg[0])
							else:
								self.msg(source, "This channel does not meet the requirements. Please try again later.")
						else:
							self.msg(source, "You need to be an operator in " + arg[0] + " to request services.")
					else:
						self.msg(source, "Channel " + arg[0] + " is suspended: " + self.suspended(arg[0]))
				else:
					self.msg(source, "Channel %s is already registered" % arg[0])
			else:
				self.msg(source, "Invalid channel: {0}".format(arg[0]))
		else:
			self.msg(source, "Syntax: REQUEST <#channel>")
