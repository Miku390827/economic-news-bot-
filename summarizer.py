import os
import google.generativeai as genai
from news_fetcher import Article

_PROMPT_TEMPLATE = """
以下の経済ニュース記事を読んで、日本語で簡潔に要約してください。

ルール:
- 箇条書き3点以内（各点は1〜2文）
- 専門用語は平易な言葉で補足する
- 出力形式: 箇条書きのみ（前置き・後書き不要）

【記事タイトル】
{title}

【記事内容】
{body}
"""

_COMBINED_PROMPT = """
以下の経済ニュース要約をまとめて、LINE通知用のメッセージを作成してください。

【本日の経済ニュース要約】を冒頭に付け、各記事を番号付きで整理してください。
最後に「詳細は各リンクから確認できます」と添えてください。

{summaries}
"""


def _get_model():
    api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def summarize_article(model, article: Article) -> str:
    body = article.summary or article.title
    prompt = _PROMPT_TEMPLATE.format(title=article.title, body=body)
    response = model.generate_content(prompt)
    return response.text.strip()


def build_message(articles: list[Article]) -> str:
    model = _get_model()

    sections = []
    for i, article in enumerate(articles, 1):
        bullets = summarize_article(model, article)
        section = f"📰 {i}. {article.title}\n{bullets}\n🔗 {article.url}"
        sections.append(section)

    summaries_text = "\n\n".join(sections)
    prompt = _COMBINED_PROMPT.format(summaries=summaries_text)
    response = model.generate_content(prompt)
    return response.text.strip()
