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

class cmd_4_domaincheck(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "DOMAINCHECK"
  HELP = "Shows you a domain lookup result"
  NEED_OPER = 1
  BOT_ID = '4'

  def onCommand(self, uid, args):
    arg = args.split()
    
    if len(arg) == 1:
      from subprocess import Popen, PIPE
      self.msg(uid, ".-: Domain-Check :-.")
      self.msg(uid)
      domain = Popen(["whois", arg[0]], stdout=PIPE).stdout.read().splitlines()
      
      for line in domain:
        if line != "" and line[0] != "%" and line[0] != "#":
          if line[0] == "[" and line[-1] == "]":
            self.msg(uid)
            
          self.msg(uid, line)
        elif line.lower().find("error") != -1:
          self.msg(uid, line)
          
      self.msg(uid)
      self.msg(uid, ".-: End of Domain-Check :-.")
    else:
      self.msg(uid, "Syntax: DOMAINCHECK <domain>")
