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
import time
from fnmatch import fnmatch as wmatch

class cmd_4_trust(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "TRUST"
    HELP = "Manage the IP trusts of your network"
    NEED_OPER = 1
    BOT_ID = '4'

    def onCommand(self, uid, args):
        arg = args.split()
        
        if len(arg) == 1:
            if arg[0].lower() == "list":
                current_timestamp = int(time.time())
                self.msg(uid, "-=- List of Trusts -=-")
                
                result = self.query("SELECT id, address, \"limit\", timestamp FROM \"trust\"")
                for row in result:
                    id = str(row["id"])
                    address = str(row["address"])
                    limit = str(row["limit"])
                    timestamp = self.convert_timestamp(int(int(row["timestamp"])- current_timestamp))
                    
                    self.msg(uid, "ID: {0}  Address: {1}  Limit: {2}  Time left: {3}".format(id, address, limit, timestamp))
                    
                self.msg(uid, "-=- End of list -=-")
            else:
                self.msg(uid, "Syntax: TRUST <set|update|del|list|search> [<address|id> [<time (in days)> [<limit>]]]")
        elif len(arg) == 2:
            if arg[0].lower() == "search":
                current_timestamp = int(time.time())
                self.msg(uid, "-=- List of Trusts (lookup parameter: " + arg[1] + ") -=-")
                
                result = self.query("SELECT id, address, \"limit\", timestamp FROM \"trust\" WHERE id LIKE %s OR address LIKE %s", "%" + arg[1][1:] + "%", "%" + arg[1] + "%")
                for row in result:
                    id = str(row["id"])
                    address = str(row["address"])
                    limit = str(row["limit"])
                    timestamp = self.convert_timestamp(int(int(row["timestamp"])- current_timestamp))
                    
                    self.msg(uid, "ID: {0}  Address: {1}  Limit: {2}  Time left: {3}".format(id, address, limit, timestamp))
                    
                self.msg(uid, "-=- End of list -=-")
            elif arg[0].lower() == "del":
                result = self.query("SELECT id, address, \"limit\" FROM \"trust\" WHERE address = %s", arg[1])
                    
                for row in result:
                    self.query("DELETE FROM trust WHERE id = %s", row["id"])
                    self.msg(uid, "#Trust# " + str(row["address"]) + " (Limit: " + str(row["limit"]) + ") removed")
                    
                self.msg(uid, "Done.")
            else:
                self.msg(uid, "Syntax: TRUST <set|update|del|list|search> [<address|id> [<time (in days)> [<limit>]]]")
        elif len(arg) == 4:
            if arg[0].lower() == "set":
                if arg[2].isdigit() and arg[3].isdigit():
                    tuid = arg[1]
                    ttime = int(arg[2])
                    tlimit = int(arg[3])
                    
                    if tuid != "0.0.0.0" and (wmatch(tuid, "*.*") or wmatch(tuid, "*:*")):
                        for row in self.query("SELECT id FROM \"trust\" WHERE address = %s", tuid):
                            self.msg(uid, "This entry is already active (ID #" + str(row["id"]) + ")!")
                            return 0
                            
                        etime = int(time.time()) + int(ttime * 60 * 60 * 24)
                        self.query("INSERT INTO \"trust\" (address, \"limit\", timestamp) VALUES (%s, %s, %s)", tuid, tlimit, etime)
                        
                        for row in self.query("SELECT uid FROM online WHERE address = %s OR host = %s", tlimit, tlimit):
                            self.checkconnection(row["uid"])
                            
                        self.msg(uid, "Done.")
                        self.send_to_op("#Trust# " + tuid + " added (Limit: " + str(tlimit) + ", Time left: " + self.convert_timestamp(int(ttime * 60 * 60 * 24)) + ")")
                    else:
                        self.msg(uid, "Denied.")
                else:
                    self.msg(uid, "Syntax: TRUST <set|update|del|list|search> [<address|id> [<time (in days)> [<limit>]]]")
            elif arg[0].lower() == "update":
                if arg[2].isdigit() and arg[3].isdigit():
                    tuid = arg[1]
                    ttime = int(arg[2])
                    tlimit = int(arg[3])
                    
                    if tuid != "0.0.0.0" and (wmatch(tuid, "*.*") or wmatch(tuid, "*:*")):
                        for row in self.query("SELECT id FROM trust WHERE address = %s", tuid):
                            etime = int(time.time()) + int(ttime * 60 * 60 * 24)
                            self.query("UPDATE \"trust\" SET timestamp = %s, \"limit\" = %s WHERE id = %s", etime, tlimit, row["id"])
                            
                            for row in self.query("SELECT uid FROM online WHERE address = %s OR host = %s", tuid, tuid):
                                self.checkconnection(row["uid"])
                                
                            self.msg(uid, "Done.")
                            self.send_to_op("#Trust# " + tuid + " updated (Limit: " + str(tlimit) + ", Time left: " + self.convert_timestamp(int(ttime * 60 * 60 * 24)) + ")")
                            return 0
                            
                        self.msg("Failed. There is no such record.")
                    else:
                        self.msg(uid, "Denied.")
                else:
                    self.msg(uid, "Syntax: TRUST <set|update|del|list|search> [<address|id> [<time (in days)> [<limit>]]]")
            else:
                self.msg(uid, "Syntax: TRUST <set|update|del|list|search> [<address|id> [<time (in days)> [<limit>]]]")
        else:
            self.msg(uid, "Syntax: TRUST <set|update|del|list|search> [<address|id> [<time (in days)> [<limit>]]]")
