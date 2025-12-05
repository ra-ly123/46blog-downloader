from scraper.posts import get_member_posts
from scraper.save import save_post
from data.members import members_data
from pathlib import Path   # ← 追加

def main():
    groups = {
        1: ("nogizaka", "乃木坂46"),
        2: ("sakurazaka", "櫻坂46"),
        3: ("hinatazaka", "日向坂46"),
        4: ("keyakizaka", "欅坂46")
    }

    print("グループを選択:")
    for num, (_, name) in groups.items():
        print(f"{num}: {name}")

    try:
        group_choice = int(input("番号を入力: ").strip())
        if group_choice not in groups:
            print("無効な番号")
            return
        group_key, group_name = groups[group_choice]
    except:
        print("番号を正しく入力してください。")
        return

    members = members_data.get(group_key, {})
    if not members:
        print("メンバーリストが空")
        return

    print("メンバーを選択:")
    for i, name in enumerate(members.keys(), start=1):
        print(f"{i}: {name}")

    try:
        choice = int(input("番号を入力: ").strip())
        if choice < 1 or choice > len(members):
            print("無効な番号")
            return
        member_name = list(members.keys())[choice - 1]
    except:
        print("番号を正しく入力してください。")
        return

    ct_id = members[member_name]
    
    # ↓↓↓  保存先を変えたい場合はこの行をいじる  ↓↓↓ #
    save_dir = Path("blog") / group_key / member_name
    # ↑↑↑  保存先を変えたい場合はこの行をいじる  ↑↑↑ #
    save_dir.mkdir(parents=True, exist_ok=True)

    page = 0

    print(f"\n=== {group_name} - {member_name} のブログ取得開始 ===\n")
    while True:
        print(f"ページ {page} を取得中…")
        posts = get_member_posts(group_key, ct_id, page=page)
        if not posts:
            print("全ページ取得完了")
            break

        for p in posts:
            success = save_post(group_key, p, save_dir=save_dir)
            if not success:
                print("全ページ取得完了")
                print(f"\n{group_name} {member_name} の全ブログ保存が完了")
                return

        page += 1

    print(f"\n{group_name} {member_name} の全ブログ保存が完了")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"予期せぬエラーが発生: {e}")
    finally:
        input("\nEnterキーで終了...")
