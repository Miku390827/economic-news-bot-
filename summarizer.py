import os
import google.generativeai as genai
from news_fetcher import Article

_PROMPT = """
以下の経済ニュース記事{count}件を読んで、LINE通知用のメッセージを日本語で作成してください。

ルール:
- 冒頭に「【本日の経済ニュース】」を付ける
- 各記事を番号付きで整理する
- 1記事につき箇条書き2点以内（各点は1文）
- 専門用語は平易な言葉で補足する
- 各記事の末尾にURLを載せる
- 最後に「詳細は各リンクから確認できます」を付ける

{articles}
"""


def build_message(articles: list[Article]) -> str:
    api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    articles_text = ""
    for i, a in enumerate(articles, 1):
        body = (a.summary or a.title)[:300]
        articles_text += f"【記事{i}】\nタイトル: {a.title}\n内容: {body}\nURL: {a.url}\n\n"

    prompt = _PROMPT.format(count=len(articles), articles=articles_text)
    response = model.generate_content(prompt)
    return response.text.strip()
