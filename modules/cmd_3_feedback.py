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

class cmd_3_feedback(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "FEEDBACK"
	HELP = "Sends your feedback about us to us"
	NEED_AUTH = 1
	BOT_ID = '3'

	def onCommand(self, source, args):
		
		if len(args) > 0:
			entry = False
			
			for data in self.query("select text from feedback where user = ?", self.auth(source)):
				entry = True
				
			if not entry:
				self.query("insert into feedback values(?, ?)", self.auth(source), args)
				self.msg(source, "Feedback added to queue.")
				
				for op in self.query("select uid from opers"):
					self.msg(str(op["uid"]), "New feedback from %s" % self.auth(source))
			else:
				self.msg(source, "You already sent a feedback. Please wait until an operator read it.")
		else:
			self.msg(source, "FEEDBACK <text>")
