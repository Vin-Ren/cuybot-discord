import api.data_lirik as api
import helper.constants as c
import helper.embeed as d
import helper.command_help as cmd
from discord.ext import commands

command = next(filter(lambda x: x['name'] == "lirik", cmd.list_help_cmd))
class Lirik(c.cog):
    def __init__(self, client):
        self.client = client

    @c.cmd.command(aliases=command["alias"])
    @commands.cooldown(1, command["cooldown"], commands.BucketType.user)
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