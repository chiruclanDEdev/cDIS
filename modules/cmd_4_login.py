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
from hashlib import sha256

class cmd_4_login(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "LOGIN"
    HELP = "Prepares your oper account for login"
    BOT_ID = '4'
    
    def onCommand(self, uid, args):
        arg = args.split()
        
        if len(arg) == 2:
            username = arg[0]
            password = sha256(bytes(arg[1], "UTF-8")).hexdigest();
            
            rows = int(self.query("SELECT COUNT(*) FROM ircd_opers WHERE username = %s AND password = %s", username, password)[0]["count"])
            if rows == 1:
                self.query("UPDATE ircd_opers SET hostname = %s WHERE username = %s AND password = %s", self.userhost(uid), username, password)
                self.msg(uid, "Done.")
            else:
                self.msg(uid, "Denied.")
        else:
            self.msg(uid, "Syntax: LOGIN <username> <password>")