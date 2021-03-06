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

class mod_3_kick(cDISModule):
    MODULE_CLASS = "KICK"
    BOT_ID = '3'
    
    def onData(self, data):
        arg = data.split()
        knick = arg[0][1:]
        kchan = arg[2]
        ktarget = self.uid(arg[3])
        kreason = ' '.join(arg[4:])[1:]
        
        if ktarget == self.bot:
            self.join(kchan)
        else:
            self.query("delete from chanlist where channel = %s and uid = %s", kchan, ktarget)