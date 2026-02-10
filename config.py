GROUPS = {
    1: ("nogizaka", "乃木坂46"),
    2: ("sakurazaka", "櫻坂46"),
    3: ("hinatazaka", "日向坂46"),
    4: ("keyakizaka", "欅坂46")
}

GROUP_SETTINGS = {
    "nogizaka": {
        "base_url": "https://www.nogizaka46.com",
        "list_url": "https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ct={ct_id}&page={page}",
        "title_selector": "h1",
        "date_selector": "p.date, time",
        "body_selector": "div.bd--edit",
    },
    "hinatazaka": {
        "base_url": "https://www.hinatazaka46.com",
        "list_url": "https://www.hinatazaka46.com/s/official/diary/member/list?ct={ct_id}&page={page}",
        "title_selector": "div.c-blog-article__title",
        "date_selector": "div.c-blog-article__date time",
        "body_selector": "div.c-blog-article__text, p",
    },
    "sakurazaka": {
        "base_url": "https://sakurazaka46.com",
        "list_url": "https://sakurazaka46.com/s/s46/diary/blog/list?ct={ct_id}&page={page}",
        "title_selector": "h1.title",
        "date_selector": "div.txt p.date.wf-a, div.box-article p.date.wf-a",
        "body_selector": "div.gmail_quote.gmail_quote_container, div.box-article, div.txt",
    },
    "keyakizaka": {
        "base_url": "https://www.keyakizaka46.com",
        "list_url": "https://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000&page={page}&ct={ct_id}",
        "title_selector": "div.box-ttl h3",
        "date_selector": "div.box-bottom ul li:first-child",
        "body_selector": "div.box-article",
    }
}

# メンバーリスト
MEMBERS_DATA = {
    "nogizaka": {
        "愛宕 心響": 63101, "五百城 茉央": 55396, "池田 瑛紗": 55397, "一ノ瀬 美空": 55390,
        "伊藤 理々杏": 36749, "井上 和": 55389, "岩本 蓮加": 36750, "梅澤 美波": 36751,
        "遠藤 さくら": 48006, "大越 ひなの": 63102, "岡本 姫奈": 55401, "小川 彩": 55392,
        "奥田 いろは": 55394, "海邉 朱莉": 63104, "賀喜 遥香": 48008, "金川 紗耶": 48010,
        "川﨑 桜": 55400, "川端 晃菜": 63105, "黒見 明香": 55383,
        "佐藤 璃果": 55384, "柴田 柚菜": 48013, "菅原 咲月": 55391, "鈴木 佑捺": 63106,
        "瀬戸口 心月": 63107, "田村 真佑": 48015, "筒井 あやめ": 48017, "冨里 奈央": 55393,
        "長嶋 凛桜": 63108, "中西 アルノ": 55395, "林 瑠奈": 55385, "増田 三莉音": 63109,
        "松尾 美佑": 55386, "森平 麗心": 63110, "矢久保 美緒": 48019, "矢田 萌華": 63111,
        "弓木 奈於": 55387, "吉田綾乃クリスティー": 36759,
        "３期生": 40004, "４期生": 40005, "新4期生": 40001, "5期生": 40007, "6期生リレー": 40008,
    },
    "hinatazaka": {
        "金村 美玖": 12, "河田 陽菜": 13, "小坂 菜緒": 14, "松田 好花": 18,
        "上村 ひなの": 21, "髙橋 未来虹": 22, "森本 茉莉": 23, "山口 陽世": 24,
        "石塚 瑶季": 25, "小西 夏菜実": 27, "清水 理央": 28, "正源司 陽子": 29,
        "竹内 希来里": 30, "平尾 帆夏": 31, "平岡 海月": 32, "藤嶌 果歩": 33,
        "宮地 すみれ": 34, "山下葉留花": 35, "渡辺莉奈": 36, "大田美月": 37,
        "大野愛実": 38, "片山 紗希": 39, "蔵盛 妃那乃": 40, "坂井 新奈": 41,
        "佐藤 優羽": 42, "下田 衣珠季": 43, "高井 俐香": 44, "鶴崎 仁香": 45, "松尾 桜": 46,
        "ポカ": "000",
    },
    "sakurazaka": {
        "井上 梨名": 43, "武元 唯衣": 45, "田村 保乃": 46, "藤吉 夏鈴": 47, "松田 里奈": 48,
        "森田 ひかる": 50, "山﨑 天": 51, "遠藤 光莉": 53, "大園 玲": 54, "大沼 晶保": 55,
        "幸阪 茉里乃": 56, "増本 綺良": 57, "守屋 麗奈": 58, "石森 璃花": 59, "遠藤 理子": 60,
        "小田倉 麗奈": 61, "小島 凪紗": 62, "谷口 愛季": 63, "中嶋 優月": 64, "的野 美青": 65,
        "向井 純葉": 66, "村井 優": 67, "村山 美羽": 68, "山下 瞳月": 69, "浅井 恋乃未": 70,
        "稲熊 ひな": 71, "勝又 春": 72, "佐藤 愛桜": 73, "中川 智尋": 74, "松本 和子": 75,
        "目黒 陽色": 76, "山川 宇衣": 77, "山田 桃実": 78,
    },
    "keyakizaka": {
        "上村 莉菜": "03", "尾関 梨香": "04", "小池 美波": "06", "小林 由依": "07",
        "齋藤 冬優花": "08", "菅井 友香": 11, "土生 瑞穂": 14, "原田 葵": 15,
        "守屋 茜": 18, "渡辺 梨加": 20, "渡邉 理佐": 21, "井上 梨名": 43,
        "関 有美子": 44, "武元 唯衣": 45, "田村 保乃": 46, "藤吉 夏鈴": 47,
        "松田 里奈": 48, "松平 璃子": 49, "森田 ひかる": 50, "山﨑 天": 51,
        "遠藤 光莉": 53, "大園 玲": 54, "大沼 晶保": 55, "幸阪 茉里乃": 56,
        "増本 綺良": 57, "守屋 麗奈": 58,
    }
}