from typing import Callable, Optional

import anthropic
import requests
from openai import OpenAI


def send_review_request(
    client: Callable, model: str, api_key: str, system_message: str, user_message: str
) -> Optional[str]:
    """共通のAPIリクエスト関数"""
    try:
        response = client(api_key=api_key).chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )
        return response.choices[0].message.content
    except requests.RequestException as e:
        print(f"APIエラー: リクエストエラーが発生しました: {e}")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
    return None


def request_review_gpt(
    full_content: str, changed_content: str, api_key: str, review_point: str
) -> Optional[str]:
    """GPT APIにファイルの全内容と変更内容を送信し、レビューをリクエストします。"""
    user_message = f"""
    "レビュポイント":\n{review_point}\n
    "全ファイル内容":\n```python\n{full_content}\n```\n
    "変更された内容":\n```python\n{changed_content}\n```\n
    "出力形式":\n
    ```json
    {{
        "コードの説明": "str", # ファイルに含まれているコードについて説明
        "変更点": "List[str]", # 変更された内容のリスト
        "改善点": "List[str]", # 改善点のリスト
        "レビュー結果": "str", # レビューの結果
        "commit": "bool" # レビューの結果、commitしても問題なければTrue, それ以外はFalse
    }}
    ```
    """
    system_message = """
    あなたはコードレビュー担当者です。
    与えれたPythonコードの変更をレビューポイントに従ってレビューしてください。
    出力は与えられたフォーマットに従ってjson形式で出力してください。
    """
    return send_review_request(
        OpenAI, "gpt-4o-mini", api_key, system_message, user_message
    )


def request_review_claude(
    full_content: str, changed_content: str, api_key: str, review_point: str
) -> Optional[str]:
    """Claude APIにファイルの全内容と変更内容を送信し、レビューをリクエストします。"""
    user_message = f"""
    レビューポイント:\n{review_point}\n\n
    全ファイル内容:\n{full_content}\n\n
    変更された内容:\n{changed_content}\n\n
    出力形式:\n{{
        "変更点": list[str],
        "レビュー結果": str,
        "commit": bool
    }}
    """
    system_message = """
    あなたはコードレビュー担当者です。
    与えれたPythonコードの変更をレビューポイントに従ってレビューしてください。
    出力は与えられたフォーマットに従ってjson形式で出力してください。
    """
    return send_review_request(
        anthropic.Anthropic,
        "claude-3-5-sonnet-20240620",
        api_key,
        system_message,
        user_message,
    )
