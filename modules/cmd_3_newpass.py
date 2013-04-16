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

from cDIS import cDISModule, config, bots

class cmd_3_newpass(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "NEWPASS"
  HELP = "Changes your password at " + bots.get("3", "nick") + "@" + config.get("SERVICES", "name")
  NEED_AUTH = 1
  BOT_ID = '3'

  def onCommand(self, source, args):
    arg = args.split()
    
    if len(arg) == 1:
      self.query("update users set pass = ? where name = ?", self.encode(arg[0]), self.auth(source))
      self.msg(source, """Your new password is "%s". Remember it!""" % arg[0])
    else:
      self.msg(source, "Syntax: NEWPASS <password>")
