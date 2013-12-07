from cDIS import cDISModule

class cmd_6_list(cDISModule):
  HELP = 'Lists your messages'
  NEED_AUTH = 1
  MODULE_CLASS = 'COMMAND'
  COMMAND = 'LIST'
  BOT_ID = '6'
  
  def onCommand(self, uid, args):
    account = self.auth(uid)
    self.msg(uid, "<= List of memos =>")
    self.msg(uid)
    
    result = self.query("""SELECT "id", "sender", "read_state" FROM "memo" WHERE "recipient" = %s ORDER BY "read_state" ASC, "id" DESC""", account)
    if result:
      for row in result:
        msg_state = "old"
        if not row["read_state"]:
          msg_state = "new!"
          
        self.msg(uid, " => ID: {0}  From: {1}  Subject: {2} (\002{2}\002)".format(str(row["id"]), row["sender"], msg_state))
    else:
      self.msg(uid, " => Nothing to display :(")
        
    self.msg(uid)
    self.msg(uid, "<= End of list =>")
    self.msg(uid, "To read a memo type \002/MSG %s READ <ID>\002" % self.bot_nick)