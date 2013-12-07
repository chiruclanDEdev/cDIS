from cDIS import cDISModule

class cmd_6_send(cDISModule):
  HELP = "Send a message to someone"
  NEED_AUTH = 1
  MODULE_CLASS = "COMMAND"
  COMMAND = "SEND"
  BOT_ID = '6'
  
  def onCommand(self, uid, args):
    arg = args.split()
    account = self.auth(uid)
    
    if len(arg) > 3:
      user = self.user(arg[1])
      if not user:
        self.msg(uid, "No such user '%s'." % arg[1])
        return 0
        
      subject = "No subject"
      message = ' '.join(arg[2:])
      if (message.find(": ") != -1):
        subject = message.split(": ")[0]
        message = message.split(": ")[1]
      
      self.query("""INSERT INTO "memo" ("user", "source", "message", "read_state") VALUES (%s, %s, %s, 0)""", user, account, message)
      self.msg(uid, "Done.")
      self.memo(user)
    else:
      self.msg(uid, "Syntax: SEND <recipient> [<subject>:] <message>")
      self.msg(uid, "  You can switch to a new line using: ´")