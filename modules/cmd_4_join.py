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

class cmd_4_join(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "JOIN"
    HELP = "Forces a user to join a channel"
    NEED_OPER = 1
    BOT_ID = '4'

    def onCommand(self, uid, args):
        arg = args.split()
        
        if len(arg) == 2:
            userData = self.GetUserData(self.uid(arg[1]))
            self.send_bot("INVITE " + userData["uid"] + " " + arg[0])
            self.send_bot("SVSJOIN " + userData["uid"] + " " + arg[0])
            self.msg(uid, "Done.")
        else:
            self.msg(uid, "Syntax: JOIN <#channel> <nick>")
