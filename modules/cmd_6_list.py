from cDIS import cDISModule

class cmd_6_list(cDISModule):
  HELP = 'Lists your messages'
  NEED_AUTH = 1
  MODULE_CLASS = 'COMMAND'
  COMMAND = 'LIST'
  BOT_ID = '6'
  
  def onCommand(self, uid, args):
    arg = args.split()
    
    if len(arg) == 0:
      self.msg(uid, "<= List of memos =>")
      self.msg(uid)
      
      result = self.query("""SELECT COUNT(*), "id", "sender", "read_state" FROM "memo" WHERE "recipient" = %s ORDER BY "read_state" ASC, "id" DESC""", account)
      for row in result:
        if int(row["count"]) == 0:
          self.msg(uid, " => Nothing to display :(")
        else:
          msg_state = "old"
          if row["read_state"]:
            msg_state = "new!"
            
          self.msg(uid, " => ID: {0}  From: {1}  Subject: {2} (\002{2}\002)".format(str(row["id"]), row["source"], msg_state))
          
      self.msg(uid)
      self.msg(uid, "<= End of list =>")
      self.msg(uid, "To read a memo type \002MEMO READ <ID>\002")
    else:
      self.msg(uid, "<= List of memos =>")
      self.msg(uid)
      
      result = self.query("""SELECT COUNT(*), "id", "sender", "read_state" FROM "memo" WHERE "recipient" = %s AND LOWER("subject") LIKE LOWER("%%s%") ORDER BY "read_state" ASC, "id" DESC""", account, args)
      for row in result:
        if int(row["count"]) == 0:
          self.msg(uid, " => No message found matching search parameters :(")
        else:
          msg_state = "old"
          if row["read_state"]:
            msg_state = "new!"
            
          self.msg(uid, " => ID: {0}  From: {1}  Subject: {2} (\002{2}\002)".format(str(row["id"]), row["source"], msg_state))
          
      self.msg(uid)
      self.msg(uid, "<= End of list =>")
      self.msg(uid, "To read a memo type \002MEMO READ <ID>\002")