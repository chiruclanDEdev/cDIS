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

from cDIS import cDISModule, config
import time

class cmd_0_tickets(cDISModule):
  HELP = "Manage tickets for {0}".format(config.get("OFFICIAL_CHANNELS", "support"))
  MODULE_CLASS = "COMMAND"
  COMMAND = "TICKETS"
  NEED_OPER = 1
  BOT_ID = '0'
  
  def onCommand(self, uid, args):
    arg = args.split()
    aResults = self.query("""SELECT COUNT(*) FROM "tickets\"""")
    if (self.db_rows == 1):
      iTicketCount = int(aResults[0]["count"])
      iPageCount = int(iTicketCount / 5)
    else:
      iTicketCount = 0
      iPageCount = 0
    
    if (len(arg) == 1):
      if (arg[0].lower() == "list"):
        self.msg(uid, "<= Ticketlist (page 1 of {0}) =>".format(iPageCount))
        
        for row in self.query("""SELECT "account" FROM "tickets" LIMIT 5"""):
          self.msg(uid, " - " + row["account"])
          
        self.msg(uid, "<= End of list =>")
      else: self.printSyntax(uid)
    elif (len(arg) == 2):
      if (arg[0].lower() == "list" and arg[1].isnumeric()):
        iPage = int(arg[1])
        if (iPage <= iPageCount):
          self.msg(uid, "<= Ticketlist (page {0} of {1}) =>".format(iPage, iPageCount))
          
          for row in self.query("""SELECT "account" FROM "tickets" LIMIT 5 OFFSET %s""", iPage * 5):
            self.msg(uid, " - " + row["account"])
            
          self.msg(uid, "<= End of list =>")
        else:
          self.msg(uid, "No such page.")
      elif (arg[0].lower() == "search"):
        self.msg(uid, "<= Ticketlist (pattern: '{0}') =>".format(arg[1]))
        
        for row in self.query("""SELECT "account" FROM "tickets" WHERE LOWER("account") LIKE LOWER(%s)""", "%" + arg[1] + "%"):
          self.msg(uid, " - " + row["account"])
          
        self.msg(uid, "<= End of list =>")
      elif (arg[0].lower() == "remove"):
        self.query("""DELETE FROM "tickets" WHERE LOWER("account") = LOWER(%s)""", arg[1])
        
        if (self.db_row == 1):
          self.msg(uid, "Done.")
        else:
          self.msg(uid, "No such ticket.")
      else: self.printSyntax(uid)
    elif (len(arg) > 2):
      if (arg[0].lower() == "add"):
        accountData = self.GetAccountData(arg[1])
        
        if accountData:
          for c in self.query("""SELECT COUNT(*) FROM "tickets" WHERE "account" = %s""", accountData["name"]):
            if (c["count"] == 0):
              sSubject = ' '.join(arg[2:])
              sMessage = """You've received a support ticket.`Subject: "{0}"`To use it type: \002/MSG G TICKET\002""".format(sSubject)
              self.query("""INSERT INTO "tickets" ("account", "subject", "timestamp") VALUES (%s, %s, %s)""", accountData["name"], sSubject, int(time.time()))
              if (self.db_rows == 1):
                self.query("""INSERT INTO "memo" ("recipient", "sender", "subject", "message", "read_state") VALUES (%s, %s, %s, %s, %s)""", accountData["name"], self.bot_nick, "You've received a support ticket.", sMessage, False)
                self.memo(accountData["name"])
                self.msg(uid, "Done.")
              else:
                self.msg(uid, "Failed.")
            else:
              self.msg(uid, "Ticket already exists.")
        else:
          self.msg(uid, "No such user.")
      else: self.printSyntax(uid)
    else: self.printSyntax(uid)
    
  def printSyntax(self, uid):
    self.msg(uid, "Syntax: {0} <LIST|SEARCH|REMOVE|ADD> [<USER> [<SUBJECT>]]".format(self.COMMAND.upper()))