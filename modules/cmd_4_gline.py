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

class cmd_4_gline(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "GLINE"
    HELP = "G-Line actions"
    NEED_OPER = 1
    BOT_ID = '4'

    def onCommand(self, uid, args):
        arg = args.split()
        
        if len(arg) == 1:
            if arg[0].lower() == "list":
                current_timestamp = int(time.time())
                self.msg(uid, "-=- List of G-lines -=-")
                
                result = self.query("SELECT id, mask, timestamp FROM glines")
                for row in result:
                    id = str(row["id"])
                    mask = str(row["mask"])
                    timestamp = self.convert_timestamp(int(int(row["timestamp"])- current_timestamp))
                    
                    
                    self.msg(uid, "ID: {id}  Hostmask: {mask}  Time left: {time_left}".format(id=id, mask=mask, time_left=timestamp))
                    
                self.msg(uid, "-=- End of list -=-")
            else:
                self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
        elif len(arg) == 2:
            if arg[0].lower() == "search":
                current_timestamp = int(time.time())
                self.msg(uid, "-=- List of G-lines (lookup parameter: " + arg[1] + ") -=-")
                
                result = self.query("SELECT id, mask, timestamp FROM glines WHERE id LIKE %s OR mask LIKE %s", "%" + arg[1][1:] + "%", "%" + arg[1] + "%")
                for row in result:
                    id = str(row["id"])
                    mask = str(row["mask"])
                    timestamp = self.convert_timestamp(int(int(row["timestamp"])- current_timestamp))
                    
                    id_mask_space = " "*int(10 - len(id))
                    mask_time_space = " "*int(25 - len(mask))
                    
                    self.msg(uid, "ID: {id}  Hostmask: {mask}  Time left: {time_left}".format(id=id, mask=mask, time_left=timestamp))
                    
                self.msg(uid, "-=- End of list -=-")
            elif arg[0].lower() == "del":
                result = self.query("SELECT id, mask FROM glines WHERE id = %s OR mask = %s", arg[1][1:], arg[1])
                    
                for row in result:
                    self.query("DELETE FROM glines WHERE id = %s", row["id"])
                    self.send_serv("GLINE " + row["mask"])
                    self.msg(uid, "#G-line# ID #" + str(row["id"]) + " removed")
                    
                self.msg(uid, "Done.")
            else:
                self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
        elif len(arg) == 3:
            if arg[0].lower() == "set":
                if arg[2].isdigit():
                    tuid = self.uid(arg[1])
                    ttime = int(arg[2])
                    
                    if not tuid.lower() == arg[1].lower():
                        if not self.isoper(tuid) and tuid != self.bot:
                            for row in self.query("SELECT id FROM glines WHERE mask = %s", "*@" + self.getip(tuid)):
                                self.msg(uid, "This entry is already active (ID #" + str(row["id"]) + ")!")
                                return 0
                                
                            etime = int(time.time()) + int(ttime * 60)
                            self.query("INSERT INTO glines (mask, timestamp) VALUES (%s, %s)", "*@" + self.getip(tuid), etime)
                            self.gline(tuid, bantime=str(int(ttime * 60)))
                            self.msg(uid, "Done.")
                        else:
                            self.msg(uid, "Denied.")
                    else:
                        self.msg(uid, "Failed. User is not online.")
                else:
                    self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
            else:
                self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
        elif len(arg) > 3:
            if arg[0].lower() == "set":
                if arg[2].isdigit():
                    tuid = self.uid(arg[1])
                    ttime = int(arg[2])
                    treason = ' '.join(arg[3:])
                    
                    if not tuid.lower() == arg[1].lower():
                        if not self.isoper(tuid) and tuid != self.bot:
                            for row in self.query("SELECT id FROM glines WHERE mask = %s", "*@" + self.getip(tuid)):
                                self.msg(uid, "This entry is already active (ID #" + str(row["id"]) + ")!")
                                return 0
                                
                            etime = int(time.time()) + int(ttime * 60)
                            self.query("INSERT INTO glines (mask, reason, timestamp) VALUES (%s, %s, %s)", "*@" + self.getip(tuid), treason, etime)
                            self.gline(tuid, treason, str(int(ttime * 60)))
                            self.msg(uid, "Done.")
                        else:
                            self.msg(uid, "Denied.")
                    else:
                        self.msg(uid, "Failed. User not online.")
                else:
                    self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
            else:
                self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
        else:
            self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
