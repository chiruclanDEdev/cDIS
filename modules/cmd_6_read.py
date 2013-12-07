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

class cmd_6_read(cDISModule):
  HELP = "Shows you the message you want to read"
  NEED_AUTH = 1
  MODULE_CLASS = "COMMAND"
  COMMAND = "READ"
  BOT_ID = '6'
  
  def onCommand(self, uid, args):
    arg = args.split()
    userData = self.GetUserData(uid)
    
    if len(arg) == 1:
      if arg[0].isnumeric():
        result = self.query("""SELECT "id", "sender", "subject", "message" FROM "memo" WHERE LOWER("recipient") = LOWER(%s) AND "id" = %s""", userData["account"], int(arg[0]))
        if result:
          row = result[0]
          self.msg(uid, "<= Message #{0} =>".format(row["id"]))
          self.msg(uid, "  \037\002Sender:\002\037  {0}".format(row["sender"]))
          self.msg(uid, "  \037\002Subject:\002\037 {0}".format(row["subject"]))
          self.msg(uid, "  \037\002Message:\002\037")
          
          for line in row["message"].split("`"):
            self.msg(uid, "    {0}".format(line))
            
          self.msg(uid, "<= Message END =>")
          self.query("""UPDATE "memo" SET "read_state" = %s WHERE "id" = %s AND LOWER("recipient") = LOWER(%s)""", True, row["id"], userData["account"])
        else:
          self.msg(uid, "Could not find message #{0}".format(arg[0]))
      else:
        self.msg(uid, "Invalid ID '{0}'.".format(arg[0]))
    else:
      self.msg(uid, "Syntax: READ <ID>")