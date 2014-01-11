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

class mod_3_mode(cDISModule):
    MODULE_CLASS = "MODE"
    BOT_ID = '3'
    
    def onData(self, data):
        smodes = data.split()[3]
        
        if smodes.find("+") != -1:
            smodes = smodes.split("+")[1]
            
            if smodes.find("-") != -1:
                smodes = smodes.split("-")[0]
                
            if smodes.find("B") != -1:
                crypthost = self.encode_md5(data.split()[0][1:] + ":" + self.nick(data.split()[0][1:]) + "!" + self.userhost(data.split()[0][1:]))
                self.send(":%s CHGHOST %s %s.gateway.%s" % (self.services_id, data.split()[0][1:], crypthost, '.'.join(self.services_name.split(".")[-2:])))
                self.query("""UPDATE "online" SET "gateway" = 1 WHERE "uid" = %s""", data.split()[0][1:])
                
        smodes = data.split()[3]
        
        if smodes.find("-") != -1:
            smodes = smodes.split("-")[1]
            
            if smodes.find("+") != -1:
                smodes = smodes.split("+")[0]
                
            if smodes.find("B") != -1:
                self.send(":%s CHGHOST %s %s" % (self.bot, data.split()[0][1:], self.gethost(data.split()[0][1:])))
                self.query("""UPDATE "online" SET "gateway" = 0 WHERE "uid" = %s""", data.split()[0][1:])