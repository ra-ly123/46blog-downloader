import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import config
from utils import sanitize_filename, shorten_title, get_date_components

def get_member_posts(group, ct_id, page=0):
    settings = config.GROUP_SETTINGS.get(group)
    if not settings:
        return []

    url = settings["list_url"].format(ct_id=ct_id, page=page)
    try:
        res = requests.get(url, timeout=15)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print(f"接続エラー: {e}")
        return []

    posts = []

    if group == "nogizaka":
        for card in soup.select("div.bl--list a.bl--card"):
            href = card.get("href")
            if not href: continue
            link = "https://www.nogizaka46.com" + href.split("?")[0]
            title = card.select_one("p.bl--card__ttl").get_text(strip=True)
            date = card.select_one("p.bl--card__date").get_text(strip=True)
            posts.append({"title": title, "date": date, "url": link})
        return posts
    
    links = []
    if group == "hinatazaka":
        links = [a.get("href") for a in soup.select("a.c-button-blog-detail")]
    elif group == "sakurazaka":
        blog_list_div = soup.select_one("div.member-blog-listm")
        if blog_list_div:
            links = [a.get("href") for a in blog_list_div.select("ul.com-blog-part li.box a") 
                     if a.get("href") and "/s/s46/diary/detail/" in a.get("href")]
    elif group == "keyakizaka":
        for side in soup.select("div.box-sideMember"): side.decompose()
        links = [a.get("href") for a in soup.select('a[href*="/s/k46o/diary/detail/"]')]

    seen = set()
    for href in links:
        if not href: continue
        link = urljoin(settings["base_url"], href.split("?")[0])
        if link not in seen:
            seen.add(link)
            posts.append({"url": link})
            
    return posts

def save_post(group, post, member_name, save_dir="blogs"):
    settings = config.GROUP_SETTINGS.get(group)
    if not settings: return False

    template_path = Path("templates") / f"{group}.html"
    if not template_path.exists():
        print(f"エラー: テンプレートファイルが見つかりません ({template_path})")
        return False

    try:
        res = requests.get(post["url"], timeout=15)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print(f"記事取得エラー: {e}")
        return False

    if "title" in post and "date" in post:
        title, date = post["title"], post["date"]
    else:
        title_elem = soup.select_one(settings["title_selector"]) or soup.select_one("title")
        title = title_elem.get_text(strip=True) if title_elem else "Unknown"
        date_elem = soup.select_one(settings["date_selector"])
        date = date_elem.get_text(strip=True) if date_elem else "Unknown"

    yyyy, mm, dd = get_date_components(date)
    body_div = soup.select_one(settings["body_selector"])
    
    if not body_div:
        return False

    safe_date = sanitize_filename(date.replace('.', '-').replace('/', '-').replace(' ', '_').replace(':', '-'))
    safe_title = sanitize_filename(shorten_title(title, 40))
    post_dir = Path(save_dir) / f"{safe_date}_{safe_title}"
    post_dir.mkdir(parents=True, exist_ok=True)
    
    text_path = post_dir / f"{safe_date}_{safe_title}.html"
    if text_path.exists():
        print(f"スキップ: 保存済み ({title})")
        return True

    base_url = settings["base_url"]
    for img in body_div.find_all("img"):
        img_url = img.get("src") or img.get("data-src") or img.get("data-original")
        if not img_url: continue

        if img_url.startswith("/"):
            img_url = urljoin(base_url, img_url)
        elif not img_url.startswith("http"):
            img_url = urljoin(post["url"], img_url)

        parsed = img_url.split("?")[0].split("#")[0]
        original_filename = os.path.basename(parsed)
        if not original_filename or "." not in original_filename:
            original_filename = "image.jpg"
        
        name_part, ext = os.path.splitext(original_filename)
        ext = ext.lower() or ".jpg"
        safe_name = sanitize_filename(name_part)
        img_filename = f"{safe_name}{ext}"
        
        img_path = post_dir / img_filename
        
        counter = 1
        stem = img_path.stem
        while img_path.exists():
            img_filename = f"{stem}_{counter}{ext}"
            img_path = post_dir / img_filename
            counter += 1

        try:
            img_res = requests.get(img_url, timeout=15)
            if img_res.status_code == 200:
                with open(img_path, "wb") as f:
                    f.write(img_res.content)
                img["src"] = img_filename
                img["alt"] = safe_name
            else:
                img.decompose()
        except:
            img.decompose()

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
        
        html_content = template_content.replace("{{title}}", title) \
                                       .replace("{{date}}", date) \
                                       .replace("{{body}}", body_div.decode_contents()) \
                                       .replace("{{YYYY}}", yyyy) \
                                       .replace("{{MM}}", mm) \
                                       .replace("{{DD}}", dd) \
                                       .replace("{{name}}", member_name)

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"保存完了: {title}")
        return True

    except Exception as e:
        print(f"保存エラー: {title} - {e}")
        return False