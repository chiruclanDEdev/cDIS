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
        
        result = self.query("SELECT COUNT(*), `id`, `source`, `read_state` FROM `memo` WHERE `user` = ? ORDER BY `read_state` ASC, `id` DESC")
        for row in result:
          if int(row["COUNT(*)"]) == 0:
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
    if len(arg) > 1:
      if arg[0].startswith("#"):
        user = arg[0][1:]
        
        if self.user(user):
          sender = self.auth(source)
          message = ' '.join(arg[1:])
          self.query("insert into memo (`user`, `source`, `message`) values (?, ?, ?)", user, sender, message)
          self.msg(source, "Done.")
          self.memo(user)
        else:
          self.msg(source, "Can't find user %s." % arg[0])
      else:
        user = self.auth(arg[0])
        
        if self.user(user):
          sender = self.auth(source)
          message = ' '.join(arg[1:])
          self.query("insert into memo (`user`, `source`, `message`) values (?, ?, ?)", user, sender, message)
          self.msg(source, "Done.")
          self.memo(user)
        else:
          self.msg(source, "Can't find user %s." % arg[0])
    else:
      self.msg(source, "Syntax: MEMO <user> <message>")
