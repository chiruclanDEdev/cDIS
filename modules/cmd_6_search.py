from cDIS import cDISModule

class cmd_6_search(cDISModule):
  HELP = "Search for a memo"
  NEED_AUTH = 1
  MODULE_CLASS = "COMMAND"
  COMMAND = "SEARCH"
  BOT_ID = '6'
  
  def onCommand(self, uid, args):
    arg = args.split()
    
    if (len(arg) > 1):
      account = self.auth(uid)
      self.msg(uid, "<= List of memos =>")
      self.msg(uid)
      
      result = self.query("""SELECT COUNT(*), "id", "sender", "read_state" FROM "memo" WHERE "recipient" = %s AND LOWER("subject") LIKE LOWER("%%s%") ORDER BY "read_state" ASC, "id" DESC""", account, args)
      for row in result:
        if int(row["count"]) == 0:
          self.msg(uid, " => Nothing found :(")
        else:
          msg_state = "old"
          if row["read_state"]:
            msg_state = "new!"
            
          self.msg(uid, " => ID: {0}  From: {1}  Subject: {2} (\002{2}\002)".format(str(row["id"]), row["source"], msg_state))
          
      self.msg(uid)
      self.msg(uid, "<= End of list =>")
      self.msg(uid, "To read a memo type \002/MSG %s READ <ID>\002" % self.bot_nick)
    else:
      self.msg(uid, "Syntax: SEARCH <pattern>")