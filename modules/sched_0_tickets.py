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

class sched_0_tickets(cDISModule):
  MODULE_CLASS = "SCHEDULE"
  NEED_OPER = 1
  BOT_ID = '0'
  TIMER = 300
  
  def onSchedule(self):
    current_timestamp = int(time.time())
    self.query("""DELETE FROM "tickets" WHERE "timestamp" < %s""", current_timestamp - 86400)
    
    if (self.db_rows > 0):
      self.send_to_op("#Tickets# {0} tickets expired.".format(self.db_rows))