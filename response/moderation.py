import helper.commands_config as cmd
import helper.constants as c
from discord.ext import commands


class Moderation(commands.cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: c.discord.Member, *, reason: str = None):
        try:
            await user.ban(reason=reason)
            await ctx.send("Banned <@{user.id}>%s".format(user=user) % ('.' if reason is None else " With Reason: '{}'.".format(reason)))
        except c.discord.NotFound:
            await ctx.send("<@{user.id}> is not found.".format(user=user))
    
    @commands.command()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: c.discord.Member, *, reason: str = None):
        try:
            user_ban_entry_exists = await ctx.message.guild.fetch_ban(user)
            if not user_ban_entry_exists:
                await ctx.send("<@{user.id}> is not found.".format(user=user))
            await user.unban(reason=reason)
            await ctx.send("Unbanned <@{user.id}>%s".format(user=user) % ('.' if reason is None else " With Reason: '{}'.".format(reason)))
        except c.discord.NotFound:
            await ctx.send("<@{user.id}> is not found.".format(user=user))
    
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
