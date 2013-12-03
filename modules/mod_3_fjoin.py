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

class mod_3_fjoin(cDISModule):
  MODULE_CLASS = "FJOIN"
  BOT_ID = '3'
  
  def onData(self, data):
    fjoin_chan = data.split()[2]
    
    for pdata in data.split()[5:]:
      pflag = pdata.split(",")[0].replace(':', '')
      pnick = pdata.split(",")[1]
      
      self.query('INSERT INTO chanlist (uid, channel, flag) VALUES (%s, %s, %s)', pnick, fjoin_chan, pflag)
      
      if self.suspended(fjoin_chan):
        if not self.isoper(pnick):
          self.kick(fjoin_chan, pnick, "Suspended: "+self.suspended(fjoin_chan))
        else:
          self.msg(fjoin_chan, "This channel is suspended: "+self.suspended(fjoin_chan))

      if self.chanexist(fjoin_chan):
        self.enforcebans(fjoin_chan)
      
      self.flag(pnick, fjoin_chan)
      
      if self.chanflag("v", fjoin_chan):
        self.mode(fjoin_chan, "+v %s" % pnick)
          
      for welcome in self.query("select name,welcome from channelinfo where name = %s", fjoin_chan):
        if self.chanflag("w", fjoin_chan):
          self.msg(pnick, "[{0}] {1}".format(welcome["name"], welcome["welcome"].replace(":topic:", self.gettopic(fjoin_chan))))
          
      if self.isoper(pnick) and self.chanexist(fjoin_chan):
        self.send(":%s NOTICE %s :Operator %s has joined" % (self.services_id, fjoin_chan, self.nick(pnick)))
        
      if self.chanflag("l", fjoin_chan):
        self.showlog(pnick, fjoin_chan)
        self.log(pnick, "join", fjoin_chan)