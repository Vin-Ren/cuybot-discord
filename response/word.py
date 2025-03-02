import api.data_dictionary as api
import helper.constants as c
from helper.commands import command


class Dictionary(c.cog):
  def __init__(self, client):
    self.client = client

  @command("kamus")
  async def Dictionary_word(self, ctx):
    bot_send = ctx.message.reply
    user_message = ctx.message.content
    message = user_message.split(" ", 1)
    data = api.get_word(message[1])
    data_word = data[0]['word']
    data_origin = data[0]['origin']
    data_phonetic = data[0]['phonetic']
    data_phonetics = data[0]['phonetics']
    data_meaning = ''
    length = len(data[0]['meanings'])
    i = 0
    idx = 0
    ids = 0
    data_synonym = ''
    data_antonym = ''
    while i < length:
      data_synonyms = data[0]['meanings'][i]['definitions'][0]['synonyms']
      if data_synonyms != []:
        while idx < len(data_synonyms) -1:
          data_synonym = data_synonym + data[0]['meanings'][i]['definitions'][0]['synonyms'][idx] + ', '
          idx += 1
          if idx == len(data_synonyms) -1:
            break 
      else:
        data_synonym = '-  '
      data_antonyms = data[0]['meanings'][i]['definitions'][0]['antonyms']
      if data_antonyms != []:
        while ids < len(data_antonyms) -1:
          data_antonym = data_antonym + data[0]['meanings'][i]['definitions'][0]['antonyms'][ids] + ', '
          ids += 1
          if ids == len(data_synonyms) -1:
            break 
      else:
        data_antonym = '-  '
      if len(data[0]['meanings'][i]['definitions'][0]) != 4:
        data_meaning = data_meaning +'\n > Kategori Kata (grammar) : '+ data[0]['meanings'][i]['partOfSpeech'] + '\nDefinisi : ' + data[0]['meanings'][i]['definitions'][0]['definition'] + '\nContoh : -' + '\nPersamaan Kata : ' + data_synonym [:-2] + '\nLawan Kata : ' + data_antonym [:-2]
      else:
        data_meaning = data_meaning +'\n > Kategori Kata (grammar) : '+ data[0]['meanings'][i]['partOfSpeech'] + '\nDefinisi : ' + data[0]['meanings'][i]['definitions'][0]['definition'] + '\nContoh : ' + data[0]['meanings'][i]['definitions'][0]['example'] + '\nPersamaan Kata : ' + data_synonym [:-2] + '\nLawan Kata : ' + data_antonym [:-2]
      i += 1
      if i == length:
        break
    if [data_phonetics] == []:
      await bot_send('kata : '+data_word+'\nPelafalan : -' + '\nAsal Muasal : ' + data_origin + data_meaning)
    elif [data_origin] == []:
      await bot_send('kata : '+data_word+'\nPelafalan : -' + data_phonetic + data_meaning)
    else:
      await bot_send('kata : '+data_word+'\nPelafalan : ' + data_phonetic + '\nAsal Muasal : ' + data_origin + data_meaning)

def setup(client):
    client.add_cog(Dictionary(client))
