# chiruclan.de IRC services
# Copyright (C) 2012-2013  Chiruclan
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
    self.query("delete from gateway where uid = ?", data.split()[2])
    self.query("delete from online where uid = ?", data.split()[2])
    self.query("delete from online where nick = ?", data.split()[4])
    self.query("insert into online values (?, ?, ?, ?, ?, '')", data.split()[2], data.split()[4], data.split()[8], data.split()[5], data.split()[7])
    self.query("UPDATE `ircd_opers` SET `hostname` = 'root@localhost` WHERE `hostname` = ?", self.userhost(data.split()[2]))
    
    result = self.query("SELECT `uid`, `key`, `value` FROM `metadata` WHERE `uid` = ? AND `key` = ?", data.split()[2], "accountname")
    for row in result:
      count = int(self.query("SELECT COUNT(*) FROM `users` WHERE `name` = ?", row["value"])[0]["COUNT(*)"])
      
      if count == 1:
        self.query("UPDATE `online` SET `account` = ? WHERE `uid` = ?", row["value"], row["uid"])
        self.msg(row["uid"], "You are now logged in as " + row["value"] + ".")
        self.vhost(row["uid"])
        self.flag(row["uid"])
        self.memo(row["value"])
      else:
        self.SetMetadata(row["uid"], row["key"])
        
    result = self.query("SELECT `id`, `mask`, `reason`, `timestamp` FROM `glines` WHERE `mask` = ? AND `timestamp` > ?", "*@"+data.split()[8], current_timestamp)
    for row in result:
      bantime = str(int(int(row["timestamp"]) - int(current_timestamp)))
      self.gline(data.split()[2], row["reason"], bantime)
      return 0
      
    self.checkconnection(data.split()[2])
    
    if data.split()[10].find("B") != -1:
      crypthost = self.encode_md5(data.split()[2] + ":" + self.nick(data.split()[2]) + "!" + self.userhost(data.split()[2]))
      self.send(":%s CHGHOST %s %s.gateway.%s" % (self.services_id, data.split()[2], crypthost, '.'.join(self.services_name.split(".")[-2:])))
      self.query("insert into gateway values (?)", data.split()[2])