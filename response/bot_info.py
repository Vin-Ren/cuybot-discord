import helper.constants as c
import helper.embeed as d
from helper.commands import command


class Bot_Info(c.cog):
    def __init__(self, client):
        self.client = client

    @command("invite")
    async def invite_bot(self,ctx):
        bot_send = ctx.message.reply

        arr = {
            "author": {"name": "CuyBot", "icon": c.bot_picture}
        }

        embed = d.embeed(
            "Invite me to your server!",
            "[**Invite CuyBot**](https://discord.com/oauth2/authorize?client_id=894421026841165826&permissions=67584&scope=bot) | [**Support Server**](https://discord.com/invite/2qp6CxN8Df)",
            "",
            arr
        )

        await bot_send(embed=embed)

    @command("status")
    async def check(self, ctx):
        bot_send = ctx.message.reply
        await bot_send(':partying_face: CuyBot Masih Aktif! :partying_face:')

    @command("hi")
    async def message(self, ctx):
        bot_send = ctx.message.reply
        await bot_send(':partying_face: Oy cuy! :partying_face: \n\nperkenalkan cuy gw bot buatannya dea dan tim :yum:\ngw siap bantu ngasih info info sesuatu yang lu butuhin')

def setup(client):
    client.add_cog(Bot_Info(client))
