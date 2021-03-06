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

class mod_0_uid(cDISModule):
    MODULE_CLASS = "UID"
    
    def onData(self, data):
        current_timestamp = int(time.time())
        self.query("""DELETE FROM "online" WHERE "uid" = %s""", data.split()[2])
        self.query("""DELETE FROM "online" WHERE "nick" = %s""", data.split()[4])
        self.query("""INSERT INTO "online" ("uid", "nick", "address", "host", "username", "account", "gateway") VALUES (%s, %s, %s, %s, %s, NULL, 0)""", data.split()[2], data.split()[4], data.split()[8], data.split()[5], data.split()[7])
        
        result = self.query("SELECT uid, key, value FROM metadata WHERE uid = %s AND key = %s", data.split()[2], "accountname")
        for row in result:
            count = int(self.query("SELECT COUNT(*) FROM users WHERE name = %s", row["value"])[0]["count"])
            
            if count == 1:
                self.query("UPDATE online SET account = %s WHERE uid = %s", row["value"], row["uid"])
                self.msg(row["uid"], "You are now logged in as " + row["value"] + ".")
                self.vhost(row["uid"])
                self.flag(row["uid"])
                self.memo(row["value"])
            else:
                self.SetMetadata(row["uid"], row["key"])
                
        result = self.query("SELECT id, mask, reason, timestamp FROM glines WHERE mask = %s AND timestamp > %s", "*@"+data.split()[8], current_timestamp)
        for row in result:
            bantime = str(int(int(row["timestamp"]) - int(current_timestamp)))
            self.gline(data.split()[2], row["reason"], bantime)
            return 0
            
        self.checkconnection(data.split()[2])
        
        if data.split()[10].find("B") != -1:
            crypthost = self.encode_md5(data.split()[2] + ":" + self.nick(data.split()[2]) + "!" + self.userhost(data.split()[2]))
            self.send(":%s CHGHOST %s %s.gateway.%s" % (self.services_id, data.split()[2], crypthost, '.'.join(self.services_name.split(".")[-2:])))
            self.query("""UPDATE "online" SET "gateway" = 1 WHERE "uid" = %s""", data.split()[2])