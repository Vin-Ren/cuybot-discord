import helper.command_help as cmd
import helper.constants as c
from discord.ext import commands


class Moderation(commands.cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command(aliases=['rmuserspam'])
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def remove_spam_message(self, ctx: commands.Context, user: c.discord.Member, limit_each_channel: int = 5):
        deleted = []
        for channel in ctx.guild.text_channels:
            deleted += await channel.purge(limit=limit_each_channel, check=lambda m: m.author.id == user.id)
        await ctx.send("Deleted {deleted_count} Message(s) from <@{user.id}>.".format(user=user.id, deleted_count=len(deleted)))


def setup(client:commands.Bot):
    client.add_cog(Moderation(client))
