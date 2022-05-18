import api.data_coffee as api
import helper.constants as c
import discord
from helper.commands import command


class Coffee(c.cog):
    def __init__(self, client):
        self.client = client

    @command("ngopi")
    async def find_kopi(self, ctx):
        user_message = ctx.message.content
        bot_send = ctx.message.reply

        data_coffee = api.data_coffee()
        embed = discord.Embed(color = discord.Colour.green(),description= ":coffee: ngopi dulu cuy")
        embed.set_image(url = data_coffee)
        await bot_send(embed=embed)

def setup(client):
    client.add_cog(Coffee(client))
