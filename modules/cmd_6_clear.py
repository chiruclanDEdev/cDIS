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

class cmd_6_clear(cDISModule):
  HELP = "Deletes all messages in your inbox"
  NEED_AUTH = 1
  MODULE_CLASS = "COMMAND"
  COMMAND = "CLEAR"
  BOT_ID = '6'
  
  def onCommand(self, uid, args):
    account = self.auth(uid)
    self.query("""DELETE FROM "memo" WHERE "recipient" = %s""", account)
    self.msg(uid, "Done.")