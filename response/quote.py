import api.data_quote as api
import helper.constants as c
from helper.commands import command


class Quote(c.cog):
  def __init__(self, client):
    self.client = client

  @command("quotes")
  async def find_quotes(self, ctx):
    bot_send = ctx.message.reply
    await bot_send('Tunggu sebentar saya carikan dulu quotes menarik untuk kamu ')
    data = api.get_quotes()
    await bot_send(data)

def setup(client):
    client.add_cog(Quote(client))
