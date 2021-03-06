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

class mod_0_metadata(cDISModule):
    MODULE_CLASS = "METADATA"
    
    def onData(self, data):
        if len(data.split()) == 5 and len(data.split()[4]) != 1:
            uid = data.split()[2]
            key = data.split()[3]
            value = ' '.join(data.split()[4:])[1:]
            
            self.SetMetadata(uid, key, value)
            
            if key == "accountname":
                if self.ison(uid, True):
                    self.query("UPDATE online SET account = %s WHERE uid = %s", value, uid)
                    self.msg(uid, "You are now logged in as " + value + ".")
                    self.vhost(uid)
                    self.flag(uid)