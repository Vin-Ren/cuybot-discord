import helper.embeed as d
import helper.constants as c
import helper.commands_config as cmd
from helper.commands import command


class Bot_Help(c.cog):
  def __init__(self, client):
    self.client = client

  
  @command("help")
  async def menu_help(self, ctx):
    bot_send = ctx.message.reply
    user_message = ctx.message.content

    help_message = user_message.split(" ", 1)
    select_help = ""

    if len(help_message) == 2:
      help_command = help_message[1].lower()
      try:
        select_help = next(filter(lambda x: x['name'] == help_command, cmd.commands_config_array))
      except:
        select_help = next(filter(lambda x: help_command in x['aliases'], cmd.commands_config_array))
        

      embed = d.embeed_help(
        0xFFDB00,
        select_help
      )

      await bot_send(embed=embed)
    else:
      arr = {
        "footer": {"text": "Bot masih dalam tahap pengembangan."},
        "field": [
          {
            "name": "**Normal**", 
            "value": "```\nhelp\nping\nhi\n \n \n \n \n \n \n```", 
            "inline": True
          },
          {
            "name": "**Info**", 
            "value": "```\nberita\ncovid\nquote\nhp\ntiktok\nanime\nlirik\nkamus\ndotalive```", 
            "inline": True
          },
          {
            "name": "**Game**", 
            "value": "```\nbadut\ntic\n \n \n \n \n \n \n \n```", 
            "inline": True
          },
          {
            "name": "**Lainnya**", 
            "value": "```\nwallpaper\nngopi\nusia\nusername\nwajah\nmlredeem\nrep\nwrcal\navatar \n```", 
            "inline": True
          },
        ]
      }

      embed = d.embeed(
        ":clipboard: **Cuybot Command** :clipboard:", 
        "Prefix cuy bot adalah `cuy/`, kamu bisa mendapatkan info lebih tentang command bot dengan cara `cuy/help <command>`",
        0xFFDB00, 
      arr)

      await bot_send(embed=embed)

def setup(client):
    client.add_cog(Bot_Help(client))