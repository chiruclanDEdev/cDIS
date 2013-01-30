from chiruserv import CServMod

class usermode(CServMod):
	HELP = "Shows your usermodes or changes it"
	NEED_AUTH = 1

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 0:
			for data in self.query("select modes from users where name = ?", self.auth(uid)):
				self.msg(uid, "Current modes: "+data["modes"])
		elif len(arg) == 1:
			data = self.query_row("select modes from users where name = ?", self.auth(uid))
			modes = self.regexflag(data["modes"], arg[0], True)
			self.query("update users set modes = ? where name = ?", ''.join([char for char in modes if char.isalpha() or char == "+" or char == "-"]), self.auth(uid))
			self.usermodes(uid)
			self.msg(uid, "Done. Current modes: " + ''.join([char for char in modes if char.isalpha() or char == "+" or char == "-"]))
		else:
			self.msg(uid, "Syntax: USERMODES [<modes>]")