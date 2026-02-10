import re

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|#\s]+', '_', name).rstrip('_')

def shorten_title(title, limit=40):
    return title[:limit] + ("…" if len(title) > limit else "")

def get_date_components(date_str):
    date_nums = re.findall(r'\d+', date_str)
    if len(date_nums) >= 3:
        return date_nums[0], date_nums[1], date_nums[2]
    return "----", "--", "--"