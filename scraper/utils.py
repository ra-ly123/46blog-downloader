import re

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|#\s]+', '_', name).rstrip('_')

def shorten_title(title, limit=40):
    return title[:limit] + ("…" if len(title) > limit else "")
