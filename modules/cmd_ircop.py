from chiruserv import CServMod
from hashlib import sha256

class cmd_ircop(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "IRCOP"
	HELP = "Manage your IRC operators"
	NEED_OPER = 1
	
	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].lower() == "list":
				self.msg(uid, "<= List of IRC operators =>")
				self.msg(uid)
				
				for row in self.query("SELECT `username`, `type` FROM `ircd_opers` ORDER BY `id`"):
					self.msg(uid, "Username: {0}  Type: {1}".format(row["username"], row["type"]))
					
				self.msg(uid)
				self.msg(uid, "<= End of list =>")
			else:
				self.msg(uid, "Syntax: IRCOP <add|delete|search|list> [<username> [<password>]]")
		elif len(arg) == 2:
			if arg[0].lower() == "search":
				self.msg(uid, "<= List of IRC operators (Search pattern: " + arg[1] + ")")
				self.msg(uid)
				
				for row in self.query("SELECT `username`, `type` FROM `ircd_opers` WHERE `username` LIKE ? ORDER BY `id`", "%" + arg[1] + "%"):
					self.msg(uid, "Username: {0}  Type: {1}".format(row["username"], row["type"]))
					
				self.msg(uid)
				self.msg(uid, "<= End of list =>")
			elif arg[0].lower() == "delete":
				if not self.isoptype(uid, "netadmin"):
					self.msg(uid, "Denied.")
					return None
					
				rows = int(self.query_row("SELECT COUNT(*) FROM `ircd_opers` WHERE `username` = ?", arg[1])["COUNT(*)"])
				
				if rows == 1:
					self.query("DELETE FROM `ircd_opers` WHERE `username` = ? AND `type` = 'GlobalOp'", arg[1])
					self.msg(uid, "Done.")
					self.msg(uid, "#IRCOP# " + arg[1] + " removed")
				else:
					self.msg(uid, "No such oper.")
			else:
				self.msg(uid, "Syntax: IRCOP <add|delete|search|list> [<username> [<password>]]")
		elif len(arg) == 3:
			if arg[0].lower() == "add":
				if not self.isoptype(uid, "netadmin"):
					self.msg(uid, "Denied.")
					return None
					
				rows = int(self.query_row("SELECT COUNT(*) FROM `ircd_opers` WHERE `username` = ?", arg[1])["COUNT(*)"])
				
				if rows == 0:
					password = sha256(arg[2]).hexdigest()
					
					self.query("INSERT INTO `ircd_opers` (`username`, `password`) VALUES (?, ?)", arg[1], password)
					self.msg(uid, "Done.")
					self.send_to_op("#IRCOP# " + arg[1] + " added")
				else:
					self.msg(uid, "User " + arg[1] + " already exists.")
		else:
			self.msg(uid, "Syntax: IRCOP <add|delete|search|list> [<username> [<password>]]")