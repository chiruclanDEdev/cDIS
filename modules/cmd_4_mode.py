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

class cmd_4_mode(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "MODE"
    HELP = "Change modes on a channel where you have no rights"
    NEED_OPER = 1
    BOT_ID = '4'

    def onCommand(self, uid, args):
        arg = args.split()
        
        if len(arg) > 1:
            if arg[0].startswith("#"):
                self.mode(arg[0], ' '.join(arg[1:]))
                self.msg(uid, "Done.")
            else:
                self.msg(uid, "Invalid channel: " + arg[0])
        else:
            self.msg(uid, "Syntax: SAMODE <#channel> <modes>")
