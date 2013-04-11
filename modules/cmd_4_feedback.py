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

class cmd_4_feedback(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "FEEDBACK"
	HELP = "Reads the feedback from users"
	NEED_OPER = 1
	BOT_ID = '4'

	def onCommand(self, source, args):
		arg = args.split()
		
		if len(args) == 0:
			self.msg(source, "Following users sent a feedback:")
			
			for data in self.query("select user from feedback"):
				self.msg(source, "  "+str(data["user"]))
				
			self.msg(source, "To read a feedback: SAFEEDBACK <user>")
		else:
			entry = False
			
			for data in self.query("select user,text from feedback where user = ?", arg[0]):
				entry = True
				self.msg(source, "[Feedback] From: %s, Message: %s" % (data["user"], data["text"]))
				self.query("delete from feedback where user = ?", str(data["user"]))
				
			if not entry:
				self.msg(source, "There is no feedback from %s" % arg[0])
