import api.data_dota as api
import helper.constants as c
from datetime import datetime
from helper.commands import command


class Dota(c.cog):
  def __init__(self, client):
    self.client = client

  @command("dotalive")
  async def dota_live(self, ctx):
    user_message = ctx.message.content
    bot_send = ctx.message.reply
    
    if any(x in user_message for x in c.request_dota):
      data = api.get_dota_live()

      i = 0
      list = 0
      live = 'Upcoming Live :'
      while list < 10:
        if 'team_name_radiant' in data[i]:
          list += 1
          live = live + '\n ' + str(list) + '. ' + data[i]['team_name_radiant'] + ' - ' + data[i]['team_name_dire'] + '(' + str(datetime.fromtimestamp(data[i]['activate_time'])) + ' UTC)'
        i += 1
      await bot_send(live)

def setup(client):
    client.add_cog(Dota(client))
