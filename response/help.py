import helper.constants as c

class bot_help(object):
  def __init__(self, user_message, bot_send):
    self.user_message = user_message
    self.bot_send = bot_send
  async def info(self):
    if any(help in self.user_message for help in c.request_help):
      return await self.bot_send(':clap: --CUYBOT HELP-- :clap:\ncommand dasar pemanggilan bot: `cuy/(command)` tanpa tada kurung\n***command yang tersedia:***\n\n*ping bot status*:\n`/status, /stat, /st, /stats, /test, /ping, /p`\n*pesan selamat datang*:\n`/help, /h, /bantuan, /command, /cmd`\n*data covid hari in*: `/covid`\n*quotes untuk memotivasi diri*:\n`/quotes, /q, /quote, /quo, /kutipan,`\n*cari lirik lagu*:\n`/lirik[spasi]judul lagu, /lirik[spasi judul lagi][nama band], /lyric[spasi nama band / judul lagu], /lyrics[spasi nama band / judul lagu], /l[spasi nama band / judul lagu]`\n*notes*: disarankan menggunakan kombinasi selengkapnya contoh: `/lirik avenged sevenfold dear god`\n\nBOT masih dalam tahap pengembangan lanjutan, untuk info lebih detail liat disini:\n`https://cuybot-discord.afrizaldea.repl.co`\n\n:wave::wave::wave:')