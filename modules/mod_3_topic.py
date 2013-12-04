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

class mod_3_topic(cDISModule):
  MODULE_CLASS = "TOPIC"
  BOT_ID = '3'
  
  def onData(self, data):
    if len(data.split()) > 1:
      if self.chanflag("t", data.split()[2]):
        for channel in self.query("select topic from channelinfo where name = %s", data.split()[2]):
          self.send(":{0} TOPIC {1} :{2}".format(self.bot, data.split()[2], channel["topic"]))