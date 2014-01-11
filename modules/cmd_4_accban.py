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

from cDIS import cDISModule, config

class cmd_4_accban(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "ACCBAN"
    HELP = "Bans an account from " + config.get("SERVICES", "description")
    NEED_OPER = 1
    BOT_ID = '4'

    def onCommand(self, uid, args):
        arg = args.split()
        
        if len(arg) == 0:
            self.msg(uid, "Account                 Reason")
            
            for data in self.query("select * from users where suspended != '0'"):
                self.msg(uid, "  {0} {1} {2}".format(data["name"], " "*int(20-len(data["name"])), data["suspended"]))
                
            self.msg(uid, "End of list.")
        elif len(arg) == 1:
            entry = False
            
            if arg[0][0] == "?":
                if self.user(arg[0][1:]):
                    self.msg(uid, "Suspend status of account " + arg[0][1:] + ": " + str(self.banned(arg[0][1:])))
                else:
                    self.msg(uid, "Can't find user " + arg[0][1:])
            else:
                if self.user(arg[0]):
                    self.query("update users set suspended = '0' where name = %s", arg[0])
                    self.msg(uid, "Done.")
                else:
                    self.msg(uid, "Can't find user " + arg[0])
        elif len(arg) > 1:
            if self.user(arg[0]):
                self.query("update users set suspended = %s where name = %s", ' '.join(arg[1:]), arg[0])
                self.msg(uid, "Done.")
            else:
                self.msg(uid, "Can't find user " + arg[0])