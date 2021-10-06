import requests
import json

def data_news(param):
    data_param = param.split()[1]
    data_news =  requests.get('https://api-berita-indonesia.vercel.app/cnn/' + data_param)
    datas = json.loads(data_news.text)
    news = datas['data']
    
    if news is None :
        return('saat ini kategori berita ' +data_param+' tidak ada\n\nmasukkan kategori berita, contoh: \n`/berita nasional`\n`/berita internasional`\n`/berita ekonomi`\n`/berita olahraga`\n`/berita teknologi`\n`/berita hiburan`')
    else:
        title = news['posts'][0]['title']
        link = news['posts'][0]['link']
        date = news['posts'][0]['pubDate']
        description = news['posts'][0]['description']
        return('Berita '+param+' hari ini: \n' + title + '\n\n' + link + '\n' + date + '\n' + description + '\n\n')
    