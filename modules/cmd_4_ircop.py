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

class cmd_4_ircop(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "IRCOP"
    HELP = "Manage your IRC operators"
    NEED_OPER = 1
    BOT_ID = '4'
    
    def onCommand(self, uid, args):
        arg = args.split()
        
        if len(arg) == 1:
            if arg[0].lower() == "list":
                self.msg(uid, "<= List of IRC operators =>")
                self.msg(uid)
                
                for row in self.query("SELECT username, type, hostname FROM ircd_opers ORDER BY id"):
                    self.msg(uid, "Username: {0}  Type: {1}  Hostname: {2}".format(row["username"], row["type"], row["hostname"]))
                    
                self.msg(uid)
                self.msg(uid, "<= End of list =>")
            else:
                self.msg(uid, "Syntax: IRCOP <add|delete|password|search|list> [<username> [<password> [<newpassword>]]]")
        elif len(arg) == 2:
            if arg[0].lower() == "search":
                self.msg(uid, "<= List of IRC operators (Search pattern: " + arg[1] + ")")
                self.msg(uid)
                
                for row in self.query("SELECT username, type, hostname FROM ircd_opers WHERE username LIKE %s ORDER BY id", "%" + arg[1] + "%"):
                    self.msg(uid, "Username: {0}  Type: {1}  Hostname: {2}".format(row["username"], row["type"], row["hostname"]))
                    
                self.msg(uid)
                self.msg(uid, "<= End of list =>")
            elif arg[0].lower() == "delete":
                if not self.isoptype(uid, "netadmin"):
                    self.msg(uid, "Denied.")
                    return None
                    
                rows = int(self.query("SELECT COUNT(*) FROM ircd_opers WHERE username = %s", arg[1])[0]["count"])
                
                if rows == 1:
                    self.query("DELETE FROM ircd_opers WHERE username = %s AND type = 'GlobalOp'", arg[1])
                    self.msg(uid, "Done.")
                    self.send_to_op("#IRCOP# " + arg[1] + " removed")
                else:
                    self.msg(uid, "No such oper.")
            else:
                self.msg(uid, "Syntax: IRCOP <add|delete|password|search|list> [<username> [<password> [<newpassword>]]]")
        elif len(arg) == 3:
            if arg[0].lower() == "add":
                if not self.isoptype(uid, "netadmin"):
                    self.msg(uid, "Denied.")
                    return None
                    
                rows = int(self.query("SELECT COUNT(*) FROM ircd_opers WHERE username = %s", arg[1])[0]["count"])
                
                if rows == 0:
                    password = sha256(bytes(arg[2], "UTF-8")).hexdigest()
                    
                    self.query("INSERT INTO ircd_opers (username, password, hostname, type) VALUES (%s, %s, 'root@localhost', 'GlobalOp')", arg[1], password)
                    self.msg(uid, "Done.")
                    self.send_to_op("#IRCOP# " + arg[1] + " added")
                else:
                    self.msg(uid, "User " + arg[1] + " already exists.")
            elif arg[0].lower() == "password":
                if not self.isoptype(uid, "netadmin"):
                    self.msg(uid, "Denied.")
                    return None
                    
                username = arg[1]
                password = sha256(bytes(arg[2], "UTF-8")).hexdigest()
                
                self.query("UPDATE ircd_opers SET password = %s WHERE username = %s", password, username)
                rows = int(self.query("SELECT COUNT(*) FROM ircd_opers WHERE username = %s AND password = %s", username, password)[0]["count"])
                
                if rows == 1:
                    self.msg(uid, "Done.")
                else:
                    self.msg(uid, "No such oper.")
            else:
                self.msg(uid, "Syntax: IRCOP <add|delete|password|search|list> [<username> [<password> [<newpassword>]]]")
        elif len(arg) == 4:
            if arg[0].lower() == "password":
                username = arg[1]
                oldpass = sha256(bytes(arg[2], "UTF-8")).hexdigest()
                newpass = sha256(bytes(arg[3], "UTF-8")).hexdigest()
                
                self.query("UPDATE ircd_opers SET password = %s WHERE username = %s AND password = %s", newpass, username, oldpass)
                rows = int(self.query("SELECT COUNT(*) FROM ircd_opers WHERE username = %s AND password = %s", username, newpass)[0]["count"])
                
                if rows == 1:
                    self.msg(uid, "Done.")
                else:
                    self.msg(uid, "Denied.")
            else:
                self.msg(uid, "Syntax: IRCOP <add|delete|password|search|list> [<username> [<password> [<newpassword>]]]")
        else:
            self.msg(uid, "Syntax: IRCOP <add|delete|password|search|list> [<username> [<password> [<newpassword>]]]")