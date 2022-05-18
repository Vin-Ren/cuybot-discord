import helper.constants as c
from discord.ext import commands
from helper.commands import command


class Moderation(c.cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @command("ban")
    async def ban(self, ctx: commands.Context, user: c.discord.Member, *, reason: str = None):
        try:
            await user.ban(reason=reason)
            await ctx.send("Banned <@{user.id}>%s".format(user=user) % ('.' if reason is None else " With Reason: '{}'.".format(reason)))
        except c.discord.NotFound:
            await ctx.send("<@{user.id}> is not found.".format(user=user))
        except Exception as exc:
            if "missing" in str(exc.args).lower():
                await ctx.send("Required permissions are missing or the user you are trying to ban have a higher authority than me.")
    
    @command("unban")
    async def unban(self, ctx: commands.Context, user: str, *, reason: str = None):
        user_check = lambda u: u == user
        not_found_message = "{user} is not found on the server ban list."
        if user.isdigit():
            userid = user
            user_check = lambda u: str(u.id) == str(userid)
            not_found_message = not_found_message.format(user="user with id={}".format(user))
        elif user.startswith("<@") and user.endswith(">"):
            userid = user[2:-1]
            user_check = lambda u: str(u.id) == str(userid)
            not_found_message = not_found_message.format(user="user {}".format(user))
        elif user.__contains__("#"):
            name, discriminator = user.split("#")
            user_check = lambda u: u.name == name and u.discriminator == discriminator
            not_found_message = not_found_message.format(user="user {}".format(user))
        else:
            await ctx.send("Given user specifier is not valid. Valid user specifier is name#discriminator or userid.")
            return
        
        banned_list = await ctx.guild.bans()
        for entry in banned_list:
            user = entry.user
            if user_check(user):
                await ctx.guild.unban(entry.user, reason=reason)
                await ctx.send("Unbanned {user.name}#{user.discriminator}%s".format(user=user) % ('.' if reason is None else " With Reason: '{}'.".format(reason)))
                return
        await ctx.send(not_found_message)
    
    @command("rmspam")
    async def remove_spam(self, ctx: commands.Context, user: c.discord.Member, limit_each_channel: int = 5):
        try:
            deleted = []
            text_channel_count = len(ctx.guild.text_channels)
            msg = await ctx.send("Deleting messages from <@{user.id}> ...".format(user=user))
            check = (lambda m: m.author.id == user.id) if user != self.client.user else (lambda m: m.author.id == user.id & m.id!=msg.id)
            for i, channel in enumerate(ctx.guild.text_channels):
                deleted += await channel.purge(limit=limit_each_channel, check=check)
                await msg.edit(content="Deleting messages from <@{user.id}> in <#{channel.id}> ({} of {} Channels) (Deleted {deleted_count} message(s))...".format(i+1, text_channel_count, user=user, channel=channel, deleted_count=len(deleted)))
            await msg.edit(content="Deleted {deleted_count} Message(s) from <@{user.id}>".format(user=user, deleted_count=len(deleted)))
        except Exception as exc:
            import sys, traceback
            exc = sys.exc_info()
            print("Encountered an error:")
            traceback.print_exception(*exc)
            raise


def setup(client:commands.Bot):
    client.add_cog(Moderation(client))
