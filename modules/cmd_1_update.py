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

from cDIS import cDISModule, shell, bots
import urllib.request, urllib.error, urllib.parse, os, _thread

class cmd_1_update(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "UPDATE"
  HELP = "Update the services"
  NEED_OPER = 1
  BOT_ID = '1'
  
  def onCommand(self, source, args):
    if not self.isoptype(source, "netadmin"):
      self.msg(source, "Denied.")
      return None
      
    _web = urllib.request.urlopen("https://raw.github.com/chiruclanDEdev/cDIS/master/version")
    _version = _web.read()
    _web.close()
    
    if open("version", "r").read() != _version:
      self.send_to_op("System: starting update...")
      _updates = len(os.listdir("sql/updates"))
      self.msg(source, "{0} -> {1}".format(open("version", "r").read(), _version))
      shell("git pull origin master")
      _files = os.listdir("sql/updates")
      __updates = len(_files)
      
      if __updates > _updates:
        while _updates != __updates:
          _updates += 1
          
          for sql in _files:
            if sql.startswith(str(_updates)+"_"):
              self.msg(source, " - Insert '{0}'".format(sql))
              file = open("sql/updates/"+sql, "r")
              
              for line in file.readlines():
                self.query(line[:1])
                
              file.close()
              
      self.msg(source, "Done.")
      
      self.send_to_op("System: completing update...")
      
      message = "Services are restarting to complete an update. We will be back soon."
      for bot in bots.sections():
        self.send(":{sid}{uuid} QUIT :{msg}".format(sid=self.services_id, uuid=bots.get(bot, "uuid"), msg=message))
      
      self.send_to_op("System: restarting...")
      self.send(":{sid} SQUIT :{msg}".format(sid=self.services_id, msg=message))
      
      _thread.interrupt_main()
      #self.msg(source, "Please note that you have to restart the services manually.")
    else:
      self.msg(source, "No update available.")