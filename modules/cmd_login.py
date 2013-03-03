from chiruserv import CServMod
from hashlib import sha256

class cmd_login(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "LOGIN"
	HELP = "Global login into oper account"
	NEED_OPER = 1
	
	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 2:
			username = arg[0]
			password = arg[1]
			sha256_password_hash = sha256(password).hexdigest()
			
			rows = int(self.query_row("SELECT COUNT(*) FROM `ircd_opers` WHERE `username` = ? AND `password` = ?", username, sha256_password_hash)["COUNT(*)"])
			
			if rows == 1:
				self.send(":{uid} OPER {user} {passwd}".format(uid=uid, user=username, passwd=password))
				self.msg(uid, "Login successful.")
			else:
				self.msg(uid, "Login failed.")
		else:
			self.msg(uid, "Syntax: LOGIN <username> <password>")