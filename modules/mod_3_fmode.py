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

class mod_3_fmode(cDISModule):
  MODULE_CLASS = "FMODE"
  BOT_ID = '3'
  
  def onData(self, data):
    if self.chanflag("l", data.split()[2]) and len(data.split()) > 4:
      self.log(data.split()[0][1:], "mode", data.split()[2], ' '.join(data.split()[4:]))
      
    if self.chanflag("m", data.split()[2]) and len(data.split()) == 5:
      if data.split()[2].startswith("#"):
        for channel in self.query("select name,modes from channelinfo where name = %s", data.split()[2]):
          self.mode(channel["name"], channel["modes"])
          
    if len(data.split()) > 5:
      if self.chanexist(data.split()[2]):
        splitted = data.split()[4]
        
        if splitted.find("+") != -1:
          splitted = splitted.split("+")[1]
          
        if splitted.find("-") != -1:
          splitted = splitted.split("-")[0]
          
        flag = self.getflag(data.split()[0][1:], data.split()[2])
        
        if flag == "h" or flag == "o" or flag == "a" or flag == self.bot_nick or flag == "n":
          if splitted.find("b") != -1:
            self.checkbans(data.split()[2], ' '.join(data.split()[5:]))
            
            for ban in data.split()[5:]:
              if fnmatch.fnmatch(ban, "*!*@*"):
                entry = False
                
                for sql in self.query("select ban from banlist where ban = %s and channel = %s", ban, data.split()[2]):
                  entry = True
                  
                if not entry and ban != "*!*@*":
                  self.query("insert into banlist (channel, ban) values (%s, %s)", data.split()[2], ban)
                  self.msg(data.split()[0][1:], "Done.")
                elif ban == "*!*@*":
                  self.msg(data.split()[2], "ACTION is angry about %s, because he tried to set a *!*@* ban." % self.nick(data.split()[0][1:]), True)
        else:
          self.mode(data.split()[2], "-{0} {1}".format("b"*len(data.split()[5:]), ' '.join(data.split()[5:])))
        
        splitted = data.split()[4]
        
        if splitted.find("-") != -1:
          splitted = splitted.split("-")[1]
          
          if splitted.find("+") != -1:
            splitted = splitted.split("+")[0]
            
          flag = self.getflag(data.split()[0][1:], data.split()[2])
          
          if flag == "h" or flag == "o" or flag == "a" or flag == self.bot_nick or flag == "n":
            if splitted.find("b") != -1:
              for ban in data.split()[5:]:
                if fnmatch.fnmatch(ban, "*!*@*"):
                  entry = False
                  
                  for sql in self.query("select ban from banlist where channel = %s and ban = %s", data.split()[2], ban):
                    entry = True
                    
                  if entry:
                    self.query("delete from banlist where channel = %s and ban = %s", data.split()[2], ban)
                    self.msg(data.split()[0][1:], "Done.")
          else:
            self.mode(data.split()[2], "+{0} {1}".format("b"*len(data.split()[5:]), ' '.join(data.split()[5:])))
            
      if self.chanflag("b", data.split()[2]):
        mchan = data.split()[2]
        splitted = data.split()[4]
        musers = data.split()[5:]
        
        if splitted.find("+") != -1:
          splitted = splitted.split("+")[1]
          
          if splitted.find("-") != -1:
            splitted = splitted.split("-")[0]
            
          if splitted.find("v") != -1:
            for user in musers:
              flag = self.getflag(self.uid(user), mchan)
              self.setuserchanflag(mchan, user, flag.replace('n', 'q'))
              
              if not self.chanflag("v", mchan) and flag != "v" and flag != "h" and flag != "o" and flag != "a" and flag != "q" and flag != "n" and self.uid(user) != self.bot:
                self.mode(mchan, "-v "+user)
                
          if splitted.find("h") != -1:
            for user in musers:
              flag = self.getflag(self.uid(user), mchan)
              self.setuserchanflag(mchan, user, flag.replace('n', 'q'))
              
              if flag != "h" and flag != "o" and flag != "a" and flag != "q" and flag != "n" and self.uid(user) != self.bot:
                self.mode(mchan, "-h "+user)
                
          if splitted.find("o") != -1:
            for user in musers:
              flag = self.getflag(self.uid(user), mchan)
              self.setuserchanflag(mchan, user, flag.replace('n', 'q'))
              
              if flag != "o" and flag != "a" and flag != "q" and flag != "n" and self.uid(user) != self.bot:
                self.mode(mchan, "-o "+user)
                
          if splitted.find("a") != -1:
            for user in musers:
              flag = self.getflag(self.uid(user), mchan)
              self.setuserchanflag(mchan, user, flag.replace('n', 'q'))
              
              if flag != "a" and flag != self.bot_nick and flag != "n" and self.uid(user) != self.bot:
                self.mode(mchan, "-a "+user)
                
              if flag != "o":
                self.mode(mchan, "-o "+user)
                
          if splitted.find(self.bot_nick) != -1:
            for user in musers:
              flag = self.getflag(self.uid(user), mchan)
              self.setuserchanflag(mchan, user, flag.replace('n', 'q'))
              
              if flag != "q" and flag != "n" and self.uid(user) != self.bot:
                self.mode(mchan, "-q "+user)
                
              if flag != "o":
                self.mode(mchan, "-o "+user)
                
      if self.chanflag("p", data.split()[2]):
        for user in data.split()[5:]:
          fm_chan = data.split()[2]
          
          for flag in self.query("""select flag from channels where channel = %s and "user" = %s""", data.split()[2], self.auth(user)):
            if flag["flag"] == "n" or flag["flag"] == "q":
              self.mode(fm_chan, "+qo {0} {0}".format(user))
            elif flag["flag"] == "a":
              self.mode(fm_chan, "+ao {0} {0}".format(user))
            elif flag["flag"] == "o":
              self.mode(fm_chan, "+o {0}".format(user))
            elif flag["flag"] == "h":
              self.mode(fm_chan, "+h {0}".format(user))
            elif flag["flag"] == "v":
              self.mode(fm_chan, "+v {0}".format(user))
            elif flag["flag"] == "b":
              self.kick(fm_chan, user, "Banned.")
              
            self.setuserchanflag(fm_chan, user, flag["flag"].replace('n', 'q'))