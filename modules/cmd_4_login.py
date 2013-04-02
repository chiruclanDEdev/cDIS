from cDIS import cDISModule
from hashlib import sha256

class cmd_4_login(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "LOGIN"
	HELP = "Prepares your oper account for login"
	BOT_ID = '4'
	
	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			username = arg[0]
			password = sha256(arg[1]).hexdigest();
			
			rows = int(self.query_row("SELECT COUNT(*) FROM `ircd_opers` WHERE `username` = ? AND `password` = ?", username, password)["COUNT(*)"])
			if rows == 1:
				self.query("UPDATE `ircd_opers` SET `hostname` = ? WHERE `username` = ? AND `password` = ?", self.userhost(uid), username, password)
				self.msg(uid, "Done.")
			else:
				self.msg(uid, "Denied.")
		else:
			self.msg(uid, "Syntax: LOGIN <username> <password>")