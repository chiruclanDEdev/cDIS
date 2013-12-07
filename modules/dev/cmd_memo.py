from cDIS import cDISModule

class cmd_memo(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "MEMO"
  HELP = "Read and write memos!"
  NEED_AUTH = 1

  def onCommand(self, uid, args):
    arg = args.split()
    account = self.auth(account)
    
    if len(arg) == 1:
      if arg[0].lower() == "list":
        self.msg(uid, "<= List of memos =>")
        self.msg(uid)
        
        result = self.query("""SELECT COUNT(*), "id", "source", "read_state" FROM "memo" WHERE "user" = %s ORDER BY "read_state" ASC, "id" DESC""", account)
        for row in result:
          if int(row["count"]) == 0:
            self.msg(uid, " => Nothing to display :(")
          else:
            msg_state = "old"
            if int(row["read_state"]) == 0:
              msg_state = "new!"
              
            self.msg(uid, " => ID: {0}  From: {1}  Subject: {2} (\002{2}\002)".format(str(row["id"]), row["source"], msg_state))
            
        self.msg(uid)
        self.msg(uid, "<= End of list =>")
        self.msg(uid, "To read a memo type \002MEMO READ <ID>\002")
    elif len(arg) == 2:
      if arg[0].lower() == "read":
        self.msg(
    if len(arg) > 3:
      if arg[0].lower() == "send":
        user = self.user(arg[1])
        if not user:
          self.msg("No such user '%s'." % arg[1])
          return 0
          
        subject = "No subject"
        message = ' '.join(arg[2:])
        if (message.find(": ") != -1):
          subject = message.split(": ")[0]
          message = message.split(": ")[1]
        
        self.query("""INSERT INTO "memo" ("user", "source", "message", "read_state") VALUES (%s, %s, %s, 0)""", user, account, message)
        self.msg(source, "Done.")
        self.memo(user)
    else:
      self.msg(source, "Syntax: MEMO <list|read|send> [<account> [[<subject>:] <message>]]")
