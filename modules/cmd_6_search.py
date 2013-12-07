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

class cmd_6_search(cDISModule):
  HELP = "Search for a memo"
  NEED_AUTH = 1
  MODULE_CLASS = "COMMAND"
  COMMAND = "SEARCH"
  BOT_ID = '6'
  
  def onCommand(self, uid, args):
    arg = args.split()
    
    if (len(arg) >= 1):
      account = self.auth(uid)
      self.msg(uid, "<= List of memos =>")
      self.msg(uid)
      
      result = self.query("""SELECT "id", "sender", "subject", "read_state" FROM "memo" WHERE "recipient" = %s AND LOWER("subject") LIKE LOWER("%%s%") ORDER BY "read_state" ASC, "id" DESC""", account, args)
      if result:
        for row in result:
          msg_state = "old"
          if not row["read_state"]:
            msg_state = "new!"
            
          self.msg(uid, " => ID: {0}  From: {1}  Subject: {2} (\002{3}\002)".format(row["id"], row["sender"], row["subject"], msg_state))
      else:
        self.msg(uid, " => Nothing found :(")
          
      self.msg(uid)
      self.msg(uid, "<= End of list =>")
      self.msg(uid, "To read a memo type \002/MSG %s READ <ID>\002" % self.bot_nick)
    else:
      self.msg(uid, "Syntax: SEARCH <pattern>")