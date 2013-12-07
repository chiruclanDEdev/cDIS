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
        for row in self.query("""SELECT COUNT(*), "id", "sender", "subject", "message" FROM "memo" WHERE LOWER("recipient") = LOWER(%s) AND "id" = %s""", userData["account"], int(arg[0])):
          if (row["count"] == 0):
            self.msg(uid, "Couldn't find message #{0} :(".format(arg[0]))
          else:
            self.msg(uid, "<= Message #{0} =>".format(row["id"]))
            self.msg(uid)
            self.msg(uid, "  Sender:  {0}".format(row["sender"]))
            self.msg(uid, "  Subject: {0}".format(row["subject"]))
            self.msg(uid, "  Message:")
            
            for line in row["message"].split(u"´"):
              self.msg(uid, "    {0}".format(line))
              
            self.msg(uid)
            self.msg(uid, "<= Message END =>")
            self.query("""UPDATE "memo" SET "read_state" = %s WHERE "id" = %s AND LOWER("recipient") = LOWER(%s)""", False, row["id"], userData["account"])
      else:
        self.msg(uid, "Invalid ID '{0}'.".format(arg[0]))
    else:
      self.msg(uid, "Syntax: READ <ID>")