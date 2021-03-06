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
from time import time

class cmd_3_resetpass(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "RESETPASS"
    HELP = "Reset your lost password"
    BOT_ID = '3'

    def onCommand(self, uid, args):
        if self.auth(uid) == '':
            arg = args.split()
            
            if len(arg) == 2:
                entry = False
                
                for data in self.query("""SELECT "name", "pass", "email", "suspended" FROM "users" WHERE "name" = %s AND "email" = %s""", arg[0], arg[1]):
                    entry = True
                    
                    if data["suspended"] == "0":
                        password = self.createPassword(config.getint("USERS", "passlen"))
                        self.query("""UPDATE "users" SET "pass" = %s WHERE "name" = %s AND "email" = %s""", password[1], data["name"], data["email"])
                        self.mail(data["email"], "Password reset", "Account: %s\nPassword: %s" % (data["name"], password[0]))
                        self.msg(uid, "I've sent an email with your lost password to %s." % data["email"])
                    else:
                        self.msg(uid, "Your account have been banned from " + self.services_description + ". Reason: " + data["suspended"])
                        
                if not entry:
                    self.msg(uid, "Can't find user " + arg[0] + " with email " + arg[1] + ".")
            else:
                self.msg(uid, "Syntax: RESETPASS <account> <email>")
        else:
            self.msg(uid, "RESETPASS is not available once you have authed.")
