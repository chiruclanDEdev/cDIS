from cDIS import cDISModule

class sched_0_trust(cDISModule):
	MODULE_CLASS = "SCHEDULE"
	NEED_OPER = 1
	BOT_ID = '0'
	TIMER = 3600
	
	def onSchedule(self):
		current_timestamp = int(time.time())
		result = self.query("SELECT `id`, `address`, `limit` FROM `trust` WHERE `timestamp` <= ?", current_timestamp)
		for row in result:
			self.query("DELETE FROM `trust` WHERE `id` = ?", row["id"])
			data = self.query("SELECT `uid` FROM `online` WHERE `address` = ? OR `host` = ?", row["address"], row["address"])
			for res in data:
				self.checkconnection(res["uid"])
				
			self.send_to_op("#Trust# " + row["address"] + " (Limit: " + str(row["limit"]) + ") expired")