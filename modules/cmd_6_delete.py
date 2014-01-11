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

class cmd_6_delete(cDISModule):
    HELP = "Deletes a message"
    NEED_AUTH = 1
    MODULE_CLASS = "COMMAND"
    COMMAND = "DELETE"
    BOT_ID = '6'
    
    def onCommand(self, uid, args):
        arg = args.split()
        
        if (len(arg) == 1):
            if (arg[0].isnumeric()):
                account = self.auth(uid)
                id = int(arg[0])
                count = self.query("""SELECT COUNT(*) FROM "memo" WHERE "recipient" = %s AND "id" = %s""", account, id)[0]["count"]
                
                if count == 1:
                    self.query("""DELETE FROM "memo" WHERE "recipient" = %s AND "id" = %s""", account, id)
                    self.msg(uid, "Done.")
                else:
                    self.msg(uid, "Couldn't locate message #{0}.".format(id))
            else:
                self.msg(uid, "Please enter a valid number.")
        else:
            self.msg(uid, "Syntax: DELETE <ID>")