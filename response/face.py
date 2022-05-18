import helper.constants as c
import api.data_face as api
import discord
from helper.commands import command, ConfigFlag


class Face(c.cog):
  def __init__(self, client):
    self.client = client

  @command("wajah")
  async def find_wajah(self, ctx):
    user_message = ctx.message.content
    bot_send = ctx.message.reply
    message = user_message.split(" ", 1)
    if len(message) == 1:
      await bot_send('masukan nama orang yang mau ditebak namanya cuy')
    else:
      data = api.get_face()
      embed = discord.Embed(color = discord.Colour.red(),description= message[1] + ' wajahnya mirip ini kan?')
      embed.set_image(url = data[0]['url'])
      await bot_send(embed=embed)

  @command("wajah", flags=ConfigFlag.COOLDOWN)
  async def avatar(self, ctx):
    user_message = ctx.message.content
    bot_send = ctx.message.reply
    message = user_message.split(" ", 1)
    if len(message) == 1:
      await bot_send('masukan namanya dulu cuy')
    else:
      embed = discord.Embed(color = discord.Colour.red(),description= ' Avatar yang cocok buat ' + message[1])
      embed.set_image(url = 'https://robohash.org/'+ message[1] + '?set=set2')
      await bot_send(embed=embed)

def setup(client):
    client.add_cog(Face(client))
