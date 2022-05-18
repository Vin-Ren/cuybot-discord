

commands_config_array = [
    {
        # root command for easy selected
        "name": "help", 
        "command": "cuy/help",
        "desc": "Menampilkan list menu command",
        "usage": "cuy/help [command]",
        "aliases": ["help"],
        "cooldown": 3
    },
    {
        "name": "status",
        "command": "cuy/status",
        "desc": "Menampilkan status bot",
        "usage": "cuy/status",
        "aliases": ["status", "stat", "stats", "test", "ping"],
        "cooldown": 3
    },
    {
        "name": "hi",
        "command": "cuy/hi",
        "desc": "Menampilkan status bot",
        "usage": "cuy/status",
        "aliases": ["hi", "helo", "hello", "halo"," hai"],
        "cooldown": 3
    },
    {
        "name": "berita",
        "command": "cuy/berita",
        "desc": "Menampilkan berita",
        "usage": "cuy/berita [kategori berita]",
        "aliases": ["berita"],
        "cooldown": 5
    },
    {
        "name": "covid",
        "command": "cuy/covid",
        "desc": "Menampilkan data menderita covid",
        "usage": "cuy/covid",
        "aliases": ["covid"],
        "cooldown": 5
    },
    {
        "name": "quotes",
        "command": "cuy/quotes",
        "desc": "Menampilkan kutipan",
        "usage": "cuy/quotes",
        "aliases": ["quotes", "quote", "kutipan"],
        "cooldown": 5
    },
    {
        "name": "hp",
        "command": "cuy/hp",
        "desc": "Menampilkan informasi hp",
        "usage": "cuy/hp [merk hp]",
        "aliases": ["hp", "mobile", "handphone", "phone"],
        "cooldown": 5
    },
    {
        "name": "tiktok",
        "command": "cuy/tiktok",
        "desc": "Menampilkan data menderita covid",
        "usage": "cuy/tiktok [username tiktok]",
        "aliases": ["tiktok", "tt"],
        "cooldown": 5
    },
    {
        "name": "anime",
        "command": "cuy/anime",
        "desc": "Menampilkan data anime",
        "usage": "cuy/anime [nama anime]",
        "aliases": ["anime", "animetod"],
        "cooldown": 5
    },
    {
        "name": "lirik",
        "command": "cuy/lirik",
        "desc": "Menampilkan lirik lagu",
        "usage": "cuy/lirik [nama lagu]",
        "aliases": ["lirik", "lyric", "lyrics"],
        "cooldown": 5
    },
    {
        "name": "kamus",
        "command": "cuy/kamus",
        "desc": "Menampilkan kata dikamus",
        "usage": "cuy/kamus [kata]",
        "aliases": ["kamus", "dict", "dictionary"],
        "cooldown": 5
    },
    {
        "name": "dotalive",
        "command": "cuy/dotalive",
        "desc": "Menampilkan jadwal live dota",
        "usage": "cuy/dotalive",
        "aliases": ["dotalive", "dota-live", "dota-stream"],
        "cooldown": 5
    },
    {
        # tictactoe
        "name": "tictactoe",
        "command": "cuy/tictactoe",
        "desc": "Main Game TicTacToe",
        "usage": "cuy/tictactoe start",
        "aliases": ["tictactoe", "tic"],
        "cooldown": 3
    },
    {
        # badut
        "name": "badut",
        "command": "cuy/badut",
        "desc": "Main Game BadutCuy",
        "usage": "cuy/badut start, cuy/atk [1 - 9], cuy/game stop",
        "aliases": ["badut"],
        "cooldown": 3
    },
    {
        "name": "wallpaper",
        "command": "cuy/wallpaper",
        "desc": "Menampilkan random wallpaper",
        "usage": "cuy/wallpaper [genre]",
        "aliases": ["wallpaper", "wp"],
        "cooldown": 5
    },
    {
        "name": "ngopi",
        "command": "cuy/ngopi",
        "desc": "Menampilkan random kopi",
        "usage": "cuy/ngopi",
        "aliases": ["ngopi","coffee", "coffee hari ini", "ngopi dulu"],
        "cooldown": 5
    },
    {
        "name": "usia",
        "command": "cuy/usia",
        "desc": "Menampilkan random usia",
        "usage": "cuy/usia [nama]",
        "aliases": ["usia"],
        "cooldown": 5
    },
    {
        "name": "username",
        "command": "cuy/username",
        "desc": "Menampilkan random username",
        "usage": "cuy/username",
        "aliases": ["username"],
        "cooldown": 3
    },
    {
        "name": "wajah",
        "command": "cuy/wajah",
        "desc": "Menampilkan random wajah",
        "usage": "cuy/wajah [nama]",
        "aliases": ["wajah", "muka"],
        "cooldown": 5
    },
    {
        "name": "avatar",
        "command": "cuy/avatar",
        "desc": "Menampilkan random avatar",
        "usage": "cuy/avatar [nama]",
        "aliases": ["avatar"],
        "cooldown": 5
    },
    {
        "name": "mlredeem",
        "command": "cuy/mlredeem",
        "desc": "mengclaim kode redeem Mobile Legends",
        "usage": "cuy/mlredeem [game id] [kode verifikasi] [kode redeem]",
        "aliases": ["mlredeem", "ml"],
        "cooldown": 5
    },
    {
        "name": "rep",
        "command": "cuy/rep",
        "desc": "mengasih reputasi kepada anggota",
        "usage": "cuy/rep help",
        "aliases": ["rep"],
        "cooldown": 5
    },
    {
        "name": "wrcal",
        "command": "cuy/wrcal",
        "desc": "menghitung win rate supaya win rate di game mobile legends menjadi lebih baik",
        "usage": "cuy/wrcal [total match] [total wr] [target wr]",
        "aliases": ["wrcal"],
        "cooldown": 5
    },
    {
        "name": "invite",
        "command": "cuy/invite",
        "desc": "Menampilkan pesan invite bot dan support server",
        "usage": "cuy/invite",
        "aliases": ["invite","inv"],
        "cooldown": 3
    }
]


moderation_config_array = [
    {
        "name": "ban",
        "command": "cuy/ban",
        "desc": "Ban seseorang dari server",
        "usage": "cuy/ban [user]",
        "aliases": ["ban"], 
        "has_perms": dict(ban_members=True),
        "bot_has_perms": dict(ban_members=True)
    },
    {
        "name": "unban",
        "command": "cuy/unban",
        "desc": "Unban seseorang dari server",
        "usage": "cuy/ban [user]",
        "aliases": ["unban"],
        "has_perms": dict(ban_members=True),
        "bot_has_perms": dict(ban_members=True)
    },
    {
        "name": "rmspam",
        "command": "cuy/rmspam",
        "desc": "Remove spam message, Purge limit on each channel is 5 on default.",
        "usage": "cuy/rmspam [user] [purge limit on each channel]",
        "aliases": ['rmspam', 'rmuserspam', 'removespam'],
        "has_perms": dict(manage_messages=True),
        "bot_has_perms": dict(manage_messages=True)
    }
]

commands_config_array += moderation_config_array

commands_config = {i['name']: i for i in commands_config_array}
