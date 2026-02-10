import re
import config
from scraper import get_member_posts, save_post

def main():
    print("グループを選択:")
    for num, (_, name) in config.GROUPS.items():
        print(f"{num}: {name}")
    
    try:
        group_choice = int(input("番号を入力: ").strip())
        if group_choice not in config.GROUPS:
            raise ValueError
        group_key, group_name = config.GROUPS[group_choice]
    except:
        print("無効な番号です。")
        return

    members = config.MEMBERS_DATA.get(group_key, {})
    if not members:
        print("メンバーリストが見つかりません。")
        return

    print("メンバーを選択:")
    member_list = list(members.keys())
    for i, name in enumerate(member_list, start=1):
        print(f"{i}: {name}")
    
    try:
        choice = int(input("番号を入力: ").strip())
        if choice < 1 or choice > len(member_list):
            raise ValueError
        member_name = member_list[choice - 1]
    except:
        print("無効な番号です。")
        return

    ct_id = members[member_name]
    clean_member_name = re.sub(r'\s+', '', member_name)
    
    # 保存先を変えたい場合はここを変更
    save_dir = f"blog/{group_key}/{clean_member_name}"
    page = 0

    print(f"\n=== {group_name} - {member_name} のブログ取得開始 ===\n")
    
    while True:
        print(f"ページ {page} を取得中…")
        posts = get_member_posts(group_key, ct_id, page=page)
        
        if not posts:
            print("これ以上記事が見つかりません。全ページ取得完了")
            break

        stop_processing = False
        for p in posts:
            success = save_post(group_key, p, member_name, save_dir=save_dir)
            
            if not success:
                print("これ以上記事が見つかりません。全ページ取得完了")
                stop_processing = True
                break
        
        if stop_processing:
            break

        page += 1

    print(f"\n{group_name} {member_name} の全ブログ保存が完了")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n中断されました。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")
    finally:
        input("\nEnterキーで終了...")