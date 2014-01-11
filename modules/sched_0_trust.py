# chiruclan.de IRC services
# Copyright (C) 2012-2014  Chiruclan
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

class sched_0_trust(cDISModule):
    MODULE_CLASS = "SCHEDULE"
    NEED_OPER = 1
    BOT_ID = '0'
    TIMER = 3600
    
    def onSchedule(self):
        current_timestamp = int(time.time())
        result = self.query("SELECT id, address, \"limit\" FROM \"trust\" WHERE timestamp <= %s", current_timestamp)
        for row in result:
            self.query("DELETE FROM \"trust\" WHERE id = %s", row["id"])
            data = self.query("SELECT uid FROM online WHERE address = %s OR host = %s", row["address"], row["address"])
            for res in data:
                self.checkconnection(res["uid"])
                
            self.send_to_op("#Trust# " + row["address"] + " (Limit: " + str(row["limit"]) + ") expired")