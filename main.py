import sys
from news_fetcher import fetch_articles
from summarizer import build_message
from line_notifier import send_line_message


def main():
    print("ニュース取得中...")
    articles = fetch_articles()
    if not articles:
        print("記事が取得できませんでした。")
        sys.exit(1)
    print(f"{len(articles)}件の記事を取得しました。")

    print("Geminiで要約中...")
    message = build_message(articles)
    print("要約完了。LINEに送信中...")

    send_line_message(message)
    print("LINE通知を送信しました。")


if __name__ == "__main__":
    main()
