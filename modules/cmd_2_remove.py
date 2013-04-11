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

from cDIS import cDISModule, bots

class cmd_2_remove(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "REMOVE"
	HELP = "Removes the channel service from your channel"
	NEED_AUTH = 1
	BOT_ID = '2'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].startswith("#"):
				if self.getflag(source, arg[0]) == "n":
					for data in self.query("select name from channelinfo where name = ?", arg[0]):
						self.query("delete from channels where channel = ?", data["name"])
						self.query("delete from channelinfo where name = ?", data["name"])
						self.query("delete from banlist where channel = ?", data["name"])
						self.msg(source, "Channel {0} has been deleted.".format(data["name"]))
						self.send(":{0} PART {1} :Channel {1} has been deleted.".format(self.services_id + bots.get("3", "uuid"), data["name"]))
				else:
					self.msg(source, "Denied.")
			else:
				self.msg(source, "Invalid channel: {0}".format(arg[0]))
		else:
			self.msg(source, "Syntax: REMOVE <#channel>")
