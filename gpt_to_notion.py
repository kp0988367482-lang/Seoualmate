"""Generate content with OpenAI and save it to Notion."""

import importlib
import os
from datetime import datetime
from typing import Any, Optional

import requests


def _load_dotenv_if_available() -> None:
    """Load .env when python-dotenv is installed, otherwise continue silently."""
    try:
        dotenv_module = importlib.import_module("dotenv")
    except ModuleNotFoundError:
        return

    load_dotenv = getattr(dotenv_module, "load_dotenv", None)
    if callable(load_dotenv):
        load_dotenv()


_load_dotenv_if_available()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


def gpt_to_notion(title: str, content: str) -> Optional[dict[str, Any]]:
    """Save generated text as a new page in a Notion database."""
    if not NOTION_TOKEN:
        raise RuntimeError("NOTION_TOKEN is not set.")
    if not NOTION_DATABASE_ID:
        raise RuntimeError("NOTION_DATABASE_ID is not set.")

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    paragraphs = [p.strip() for p in content.split("\n") if p.strip()]

    children = []
    for para in paragraphs:
        children.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": para[:2000]}}]
                },
            }
        )

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Date": {"date": {"start": datetime.now().isoformat()}},
        },
        "children": children[:100],
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=payload,
        timeout=30,
    )

    if response.status_code == 200:
        page_url = response.json().get("url", "")
        print(f"Saved to Notion: {page_url}")
        return response.json()

    print(f"Failed to save to Notion: {response.status_code} - {response.text}")
    return None


def ask_gpt_and_save(prompt: str, page_title: Optional[str] = None) -> str:
    """Generate content with OpenAI, then save it to Notion."""
    try:
        openai_module = importlib.import_module("openai")
        openai_client_cls = getattr(openai_module, "OpenAI")
    except ModuleNotFoundError as exc:
        raise RuntimeError("openai package is required. Install with: pip install openai") from exc

    client = openai_client_cls(api_key=os.getenv("OPENAI_API_KEY"))

    print("Generating response with GPT...")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    raw_content = response.choices[0].message.content
    if not isinstance(raw_content, str) or not raw_content.strip():
        raise RuntimeError("OpenAI response did not include text content.")

    content = raw_content
    title = page_title or prompt[:50]

    print("Saving generated content to Notion...")
    gpt_to_notion(title=title, content=content)
    return content


if __name__ == "__main__":
    result = ask_gpt_and_save(
        prompt="Write a short idea for an AI SaaS landing page.",
        page_title="AI SaaS Idea",
    )
    print("\n--- GPT Output ---")
    print(result)
