import os
import time
from google import genai
from news_fetcher import Article

_PROMPT = """
以下の経済ニュース{count}件を読んで、LINE通知用の日本語メッセージを作成してください。

ルール:
- 冒頭に「【本日の経済ニュース】」を付ける
- 各記事を番号付きで1〜2行で要約する
- 各記事の末尾にURLを載せる
- 最後に「詳細は各リンクから確認できます」を付ける

{articles}
"""


def build_message(articles: list[Article]) -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    articles_text = ""
    for i, a in enumerate(articles, 1):
        body = (a.summary or a.title)[:150]
        articles_text += f"【{i}】{a.title}\n{body}\nURL: {a.url}\n\n"

    prompt = _PROMPT.format(count=len(articles), articles=articles_text)

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(40)
            else:
                raise e
