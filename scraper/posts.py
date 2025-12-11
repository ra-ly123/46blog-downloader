import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_member_posts(group, ct_id, page=0):
    if group == "nogizaka":
        url = f"https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ct={ct_id}&page={page}"
        res = requests.get(url)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        posts = []
        for card in soup.select("div.bl--list a.bl--card"):
            href = card.get("href")
            if not href:
                continue
            link = "https://www.nogizaka46.com" + href.split("?")[0]
            title = card.select_one("p.bl--card__ttl").get_text(strip=True)
            date = card.select_one("p.bl--card__date").get_text(strip=True)
            posts.append({
                "title": title,
                "date": date,
                "url": link
            })
        return posts

    elif group == "hinatazaka":
        url = f"https://www.hinatazaka46.com/s/official/diary/member/list?ct={ct_id}&page={page}"
        res = requests.get(url)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        posts = []
        for a in soup.select("a.c-button-blog-detail"):
            href = a.get("href")
            if not href:
                continue
            link = urljoin("https://www.hinatazaka46.com", href.split("?")[0])
            posts.append({"url": link})
        return posts

    elif group == "sakurazaka":
        url = f"https://sakurazaka46.com/s/s46/diary/blog/list?ct={ct_id}&page={page}"
        res = requests.get(url)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        posts = []
        blog_list_div = soup.select_one("div.member-blog-listm")
        if not blog_list_div:
            return posts

        for a in blog_list_div.select("ul.com-blog-part li.box a"):
            href = a.get("href")
            if href and "/s/s46/diary/detail/" in href:
                link = urljoin("https://sakurazaka46.com", href.split("?")[0])
                posts.append({"url": link})
        return posts

    elif group == "keyakizaka":
        url = f"https://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000&page={page}&ct={ct_id}"
        res = requests.get(url)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
        posts = []
        urls = set()
        for side in soup.select("div.box-sideMember"):
            side.decompose()
        for a in soup.select('a[href*="/s/k46o/diary/detail/"]'):
            href = a.get("href")
            if not href:
                continue
            link = urljoin("https://www.keyakizaka46.com", href.split("?")[0])
            if link in urls:
                continue
            urls.add(link)
            posts.append({"url": link})
        return posts

    return []

