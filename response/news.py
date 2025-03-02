import api.data_news as api
import helper.constants as c
from helper.commands import command


class News(c.cog):
    def __init__(self, client):
        self.client = client

    @command("berita")
    async def find_berita(self, ctx):
        user_message = ctx.message.content
        bot_send = ctx.message.reply
        parameter = user_message.split()
        if len(parameter) == 1:
            await bot_send('masukkan kategori berita, contoh: \n`/berita nasional`\n`/berita internasional`\n`/berita ekonomi`\n`/berita olahraga`\n`/berita teknologi`\n`/berita hiburan`')
        else:
            daftar_news = api.data_news(user_message)
            await bot_send(daftar_news)

def setup(client):
    client.add_cog(News(client))
