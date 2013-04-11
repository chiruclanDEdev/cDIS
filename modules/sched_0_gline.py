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
import time

class sched_0_gline(cDISModule):
	MODULE_CLASS = "SCHEDULE"
	NEED_OPER = 1
	BOT_ID = '0'
	TIMER = 60
	
	def onSchedule(self):
		current_timestamp = time.time()
		
		results = self.query("SELECT `id`, `mask`, `timestamp` FROM `glines`")
		for row in results:
			expire_timestamp = int(row["timestamp"])
			
			if current_timestamp >= expire_timestamp:
				self.query("DELETE FROM `glines` WHERE `id` = ?", row["id"])
				self.send_serv("GLINE " + row["mask"])
				self.send_to_op("#G-line# Removed ID #" + str(row["id"]) + " (Hostmask: " + row["mask"] + ")")