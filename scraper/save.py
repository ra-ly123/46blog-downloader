import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

from .utils import sanitize_filename, shorten_title

def save_post(group, post, save_dir="blogs"):
    res = requests.get(post["url"])
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    group_settings = {
        "nogizaka": {
            "title_selector": "h1",
            "date_selector": "p.date, time",
            "body_selector": "div.bd--edit",
            "title_color": "#9E3EB2",
            "base_url": "https://www.nogizaka46.com"
        },
        "hinatazaka": {
            "title_selector": "div.c-blog-article__title",
            "date_selector": "div.c-blog-article__date time",
            "body_selector": "div.c-blog-article__text, p",
            "title_color": "#5BBEE4",
            "base_url": "https://www.hinatazaka46.com"
        },
        "sakurazaka": {
            "title_selector": "h1.title",
            "date_selector": "div.txt p.date.wf-a, div.box-article p.date.wf-a",
            "body_selector": "div.gmail_quote.gmail_quote_container, div.box-article, div.txt",
            "title_color": "#F19DB5",
            "base_url": "https://sakurazaka46.com"
        },
        "keyakizaka": {
            "title_selector": "div.box-ttl h3",
            "date_selector": "div.box-bottom ul li:first-child",
            "body_selector": "div.box-article",
            "title_color": "#7CCD7C",
            "base_url": "https://www.keyakizaka46.com"
        }
    }

    settings = group_settings.get(group, {})
    if not settings:
        return False

    if "title" in post and "date" in post:
        title = post["title"]
        date = post["date"]
    else:
        title_elem = soup.select_one(settings["title_selector"]) or soup.select_one("title")
        title = title_elem.get_text(strip=True) if title_elem else "Unknown"
        date_elem = soup.select_one(settings["date_selector"])
        date = date_elem.get_text(strip=True) if date_elem else "Unknown"

    body_div = soup.select_one(settings["body_selector"])
    if not body_div:
        return False

    safe_date = sanitize_filename(
        date.replace('.', '-').replace('/', '-').replace(' ', '_').replace(':', '-')
    )

    short_title = shorten_title(title, 40)
    safe_title = sanitize_filename(short_title)

    post_dir = Path(save_dir) / f"{safe_date}_{safe_title}"
    post_dir.mkdir(parents=True, exist_ok=True)

    text_path = post_dir / f"{safe_date}_{safe_title}.html"

    if text_path.exists():
        print(f"スキップ: 保存済み ({title})")
        return True

    base_url = settings["base_url"]
    for img in body_div.find_all("img"):
        img_url = img.get("src") or img.get("data-src") or img.get("data-original")
        if not img_url:
            continue

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

    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Noto Sans JP', sans-serif;
      background-color: #fff;
      color: #46464B;
      font-size: 0.8em;
      line-height: 1.8;
      margin: 20px;
    }}
    .header-section {{
      background-color: #f7f7f7;
      padding: 10px 20px;
      margin-left: -20px;
      margin-right: -20px;
      margin-bottom: 3em;
    }}
    h1 {{
      color: {settings["title_color"]};
      font-size: 1.4em;
      margin-bottom: 0.2em;
    }}
    p.date {{
      color: #9595A0;
      margin-top: 0;
      font-size: 0.6em;
      margin-bottom: 0;
    }}
    img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 1em 0;
    }}
  </style>
</head>
<body>
  <div class="header-section">
    <h1>{title}</h1>
    <p class="date">{date}</p>
  </div>
  {body_div.decode_contents()}
</body>
</html>"""

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"保存完了: {title}")
    return True
