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

class mod_3_notice(cDISModule):
	MODULE_CLASS = "NOTICE"
	BOT_ID = '3'
	
	def onData(self, data):
		if data.split()[2].startswith("#") and self.chanflag("l", data.split()[2]):
			self.log(data.split()[0][1:], "notice", data.split()[2], ' '.join(data.split()[3:]))