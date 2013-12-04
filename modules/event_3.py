from cDIS import cDISModule

class event_3(cDISModule):
  MODULE_CLASS = 'INTERNAL_EVENT'
  COMMAND = 'STARTUP'
  BOT_ID = '3'
  
  def onEvent(self, event):
    if event == 'STARTUP':
      for channel in self.query("""SELECT "name", "modes", "topic" FROM "channelinfo\""""):
        self.join(channel["name"])
        
        if self.chanflag("m", channel["name"]):
          self.mode(channel["name"], channel["modes"])
          
        if self.chanflag("t", channel["name"]):
          self.send(":{0} TOPIC {1} :{2}".format(self.bot, channel["name"], channel["topic"]))