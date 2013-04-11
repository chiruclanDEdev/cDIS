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

class mod_0_quit(cDISModule):
	MODULE_CLASS = "QUIT"
	
	def onData(self, data):
		for qchan in self.query("select * from chanlist where uid = ?", data.split()[0][1:]):
			if self.chanflag("l", qchan["channel"]):
				if len(data.split()) == 2:
					self.log(qchan["uid"], "quit", qchan["channel"])
				else:
					self.log(qchan["uid"], "quit", qchan["channel"], ' '.join(data.split()[2:])[1:])
					
		self.query("delete from chanlist where uid = ?", data.split()[0][1:])
		self.query("delete from gateway where uid = ?", str(data.split()[0])[1:])
		self.query("delete from online where uid = ?", str(data.split()[0])[1:])
		self.query("delete from opers where uid = ?", data.split()[0][1:])