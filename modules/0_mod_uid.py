from cDIS import cDISModule
import time

class 0_mod_uid(cDISModule):
	MODULE_CLASS = "UID"
	
	def onData(self, data):
		current_timestamp = int(time.time())
		self.query("delete from gateway where uid = ?", data.split()[2])
		self.query("delete from online where uid = ?", data.split()[2])
		self.query("delete from online where nick = ?", data.split()[4])
		self.query("insert into online values (?, ?, ?, ?, ?, '')", data.split()[2], data.split()[4], data.split()[8], data.split()[5], data.split()[7])
		
		result = self.query("SELECT `id`, `mask`, `reason`, `timestamp` FROM `glines` WHERE `mask` = ? AND `timestamp` > ?", "*@"+data.split()[8], current_timestamp)
		for row in result:
			bantime = str(int(int(row["timestamp"]) - int(current_timestamp)))
			self.gline(data.split()[2], row["reason"], bantime)
			return 0
			
		self.checkconnection(data.split()[2])
		
		if data.split()[10].find("B") != -1:
			crypthost = self.encode_md5(data.split()[2] + ":" + self.nick(data.split()[2]) + "!" + self.userhost(data.split()[2]))
			self.send(":%s CHGHOST %s %s.gateway.%s" % (self.services_id, data.split()[2], crypthost, '.'.join(self.services_name.split(".")[-2:])))
			self.query("insert into gateway values (?)", data.split()[2])