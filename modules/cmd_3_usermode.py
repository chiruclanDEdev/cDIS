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

class cmd_3_usermode(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "USERMODE"
  HELP = "Shows your usermodes or changes it"
  NEED_AUTH = 1
  BOT_ID = '3'

  def onCommand(self, uid, args):
    arg = args.split()
    
    if len(arg) == 0:
      for data in self.query("""SELECT "modes" FROM "users" WHERE "name" = %s""", self.auth(uid)):
        self.msg(uid, "Current modes: "+data["modes"])
    elif len(arg) == 1:
      data = self.query("""SELECT "modes" FROM "users" WHERE "name" = %s""", self.auth(uid))[0]
      modes = self.regexflag(data["modes"], arg[0], True)
      newmodes = ''.join([char for char in modes if char.isalpha() or char == "+" or char == "-"])
      self.query("""UPDATE "users" SET "modes" = %s WHERE "name" = %s""", newmodes, self.auth(uid))
      self.usermodes(uid)
      self.msg(uid, "Done. Current modes: " + ''.join([char for char in modes if char.isalpha() or char == "+" or char == "-"]))
    else:
      self.msg(uid, "Syntax: USERMODES [<modes>]")