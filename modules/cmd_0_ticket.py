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

class cmd_0_ticket(cDISModule):
  HELP = "Use a ticket you got from {0}".format(official_channels["help"])
  MODULE_CLASS = "COMMAND"
  COMMAND = "TICKET"
  NEED_AUTH = 1
  BOT_ID = '0'
  
  def onCommand(self, uid, args):
    if self.isoper(uid):
      self.send_bot("SVSJOIN {0} {1}".format(uid, official_channels["support"]))
      return 0
      
    sAccount = self.auth(uid)
    result = self.query("""SELECT "subject" FROM "tickets" WHERE "account" = %s""", sAccount)
    
    if result:
      for row in result:
        self.send_bot("SVSJOIN {0} {1}".format(uid, official_channels["support"]))
        self.query("""DELETE FROM "tickets" WHERE "account" = %s""", sAccount)
        self.msg(self.channel["support"], """User {0} joined with subject: "{1}"!""".format(sAccount, row["subject"]))
        
      self.msg(uid, "Done.")
    else:
      self.msg(uid, "Denied.")