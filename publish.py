"""
直接输入 → 发布到 Notion
简单：输入内容，按 Enter，保存完成
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def save_to_notion(title: str, content: str, use_gpt: bool = False) -> bool:
    """保存内容到 Notion"""

    # 如果要用 GPT 润色
    if use_gpt and OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            print("🤖 GPT 润色中...")
            resp = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"请帮我整理以下内容，使其更清晰易读：\n\n{content}"}]
            )
            content = resp.choices[0].message.content
            print("✅ GPT 润色完成\n")
        except Exception as e:
            print(f"⚠️  GPT 跳过: {e}\n")

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # 段落切分
    paragraphs = [p.strip() for p in content.split("\n") if p.strip()]
    children = [{
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": p[:2000]}}]
        }
    } for p in paragraphs[:100]]

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Date": {"date": {"start": datetime.now().isoformat()}}
        },
        "children": children
    }

    r = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)

    if r.status_code == 200:
        url = r.json().get("url", "")
        print(f"\n✅ 已发布到 Notion!")
        print(f"🔗 {url}\n")
        return True
    else:
        err = r.json().get("message", r.text)
        print(f"\n❌ 发布失败: {err}\n")
        return False


def check_config():
    """检查配置"""
    missing = []
    if not NOTION_TOKEN or NOTION_TOKEN == "ntn_your_token_here":
        missing.append("NOTION_TOKEN")
    if not NOTION_DATABASE_ID or NOTION_DATABASE_ID == "your_database_id_here":
        missing.append("NOTION_DATABASE_ID")
    return missing


# 分类配置 —— 每个类别对应一个 Notion Database ID
# 在 .env 里加对应的变量，没有的话统一存到 NOTION_DATABASE_ID
CATEGORIES = {
    "1": ("🎬 YouTube",   os.getenv("NOTION_DB_YOUTUBE")   or NOTION_DATABASE_ID),
    "2": ("⚙️  SaaS",     os.getenv("NOTION_DB_SAAS")      or NOTION_DATABASE_ID),
    "3": ("📢 Marketing", os.getenv("NOTION_DB_MARKETING")  or NOTION_DATABASE_ID),
    "4": ("💡 想法",       os.getenv("NOTION_DB_IDEAS")      or NOTION_DATABASE_ID),
    "5": ("📋 其他",       NOTION_DATABASE_ID),
}


def pick_category() -> tuple[str, str]:
    """选择分类，返回 (名称, database_id)"""
    print("\n📂 选择分类:")
    for key, (name, _) in CATEGORIES.items():
        print(f"   [{key}] {name}")
    choice = input("\n   输入编号 (默认5): ").strip() or "5"
    name, db_id = CATEGORIES.get(choice, CATEGORIES["5"])
    return name, db_id


def main():
    print("\n" + "━" * 50)
    print("  📝  输入 → 分类发布到 Notion")
    print("━" * 50)

    # 检查配置
    missing = check_config()
    if missing:
        print(f"\n❌ 请先在 .env 填入: {', '.join(missing)}")
        print("   文件位置: .env\n")
        sys.exit(1)

    gpt_available = bool(OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-your"))
    print(f"  Notion : ✅ 已连接")
    print(f"  GPT    : {'✅ 可用 (会自动润色)' if gpt_available else '⚪ 未配置 (直接发布)'}")
    print(f"  分类   : 🎬 YouTube / ⚙️ SaaS / 📢 Marketing / 💡 想法 / 📋 其他")
    print("━" * 50 + "\n")

    while True:
        # 选分类
        category_name, db_id = pick_category()
        print(f"   → {category_name}\n")

        # 输入标题
        title = input("📌 标题 (留空退出): ").strip()
        if not title:
            print("👋 再见！")
            break

        # 输入内容
        print("✏️  内容 (多行输入，空行结束):")
        lines = []
        while True:
            line = input("   > ")
            if line == "":
                if lines:
                    break
            else:
                lines.append(line)

        content = "\n".join(lines)

        # 发布到对应分类的 database
        global NOTION_DATABASE_ID
        _original = NOTION_DATABASE_ID
        NOTION_DATABASE_ID = db_id

        print(f"\n🚀 发布到 [{category_name}] 中...")
        save_to_notion(title, content, use_gpt=gpt_available)

        NOTION_DATABASE_ID = _original

        again = input("继续? (Enter继续 / q退出): ").strip().lower()
        if again == "q":
            print("👋 再见！")
            break
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已中断")
