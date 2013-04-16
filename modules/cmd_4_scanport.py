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

class cmd_4_scanport(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "SCANPORT"
  HELP = "Checks host for an open port"
  NEED_OPER = 1
  BOT_ID = '4'

  def onCommand(self, uid, args):
    arg = args.split()
    
    if len(arg) == 2:
      self.msg(uid, "Scanning " + arg[0] + ":" + arg[1] + " ...")
      
      if self.scanport(arg[0], arg[1]):
        self.msg(uid, arg[0] + ":" + arg[1] + ": Open.")
      else:
        self.msg(uid, arg[0] + ":" + arg[1] + ": Closed.")
    else:
      self.msg(uid, "Syntax: SCANPORT <host> <port>")