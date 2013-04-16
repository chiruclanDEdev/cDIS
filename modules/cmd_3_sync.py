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

class cmd_3_sync(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "SYNC"
  NEED_AUTH = 1
  HELP = "Syncs your flags on all channels"
  BOT_ID = '3'

  def onCommand(self, source, args):
    self.flag(source)
    self.msg(source, "Done.")