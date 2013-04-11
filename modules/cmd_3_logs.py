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

class cmd_3_logs(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "LOGS"
	HELP = "View and clear channel logs"
	NEED_AUTH = 1
	BOT_ID = '3'
	
	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			if arg[0].startswith("#"):
				flag = self.getflag(uid, arg[0])
				
				if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
					if arg[1].lower() == "view":
						self.showlog(uid, arg[0])
					elif arg[1].lower() == "clear":
						if flag == "n" or flag == "q" or flag == "a":
							self.query("DELETE FROM `logs` WHERE `channel` = ?", arg[0])
							self.msg(uid, "Done.")
						else:
							self.msg(uid, "Denied.")
					else:
						self.msg(uid, "Syntax: LOGS <#channel> <view/clear>")
				else:
					self.msg(uid, "Denied.")
		else:
			self.msg(uid, "Syntax: LOGS <#channel> <view/clear>")
			
	def onFantasy(self, uid, chan, args):
		self.onCommand(uid, chan + " " + args)