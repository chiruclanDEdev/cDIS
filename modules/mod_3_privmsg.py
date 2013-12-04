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
import builtins
import time

class mod_3_privmsg(cDISModule):
  MODULE_CLASS = "PRIVMSG"
  BOT_ID = '3'
  
  def onData(self, data):
    if self.chanexist(data.split()[2]):
      puid = data.split()[0][1:]
      pchan = data.split()[2]
      
      if self.chanflag("s", pchan):
        messages = 10
        seconds = [6, 5]
        
        for dump in self.query("select spamscan from channelinfo where name = %s", pchan):
          messages = int(dump["spamscan"].split(":")[0])
          seconds = [int(dump["spamscan"].split(":")[1]) + 1, int(dump["spamscan"].split(":")[1])]
          
        if (pchan, puid) in spamscan:
          num = spamscan[pchan,puid][0] + 1
          spamscan[pchan,puid] = [num, spamscan[pchan,puid][1]]
          timer = int(time.time()) - spamscan[pchan,puid][1]
          
          if spamscan[pchan,puid][0] == messages and timer < seconds[0]:
            if self.isoper(puid):
              self.msg(puid, "WARNING: You are flooding {0}. Please stop that, but I won't kill you because you're an IRC Operator.".format(pchan))
            else:
              self.kill(puid)
              
            del spamscan[pchan,puid]
          elif timer > seconds[1]:
            spamscan[pchan,puid] = [1, int(time.time())]
        else:
          spamscan[pchan,puid] = [1, int(time.time())]
          
    builtins.spamscan = spamscan