import api.data_lirik as api
import helper.constants as c
import helper.embeed as d
from helper.commands import command


class Lirik(c.cog):
    def __init__(self, client):
        self.client = client

    @command("lirik")
    async def find_lirik(self, ctx):
      user_message = ctx.message.content
      bot_send = ctx.message.reply
      data = user_message.split(" ", 1)
      if len(data) == 1:
        embed = d.embeed("Lirik Lagu", ':clap: ketik judul lagunya atau berikut juga dengan nama bandnya :clap:')
        await bot_send(embed=embed)
      else:
        requested_song = self.user_message.split(" ", 1)[1]
        daftar_lagu = api.get_lirik(requested_song)
        embed = d.embeed(f"Lirik Lagu {requested_song}", daftar_lagu)
        await bot_send(embed=embed)

def setup(client):
    client.add_cog(Lirik(client))
