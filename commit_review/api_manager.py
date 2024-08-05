import os

from dotenv import load_dotenv

from .request_review import request_review_claude, request_review_gpt

load_dotenv()


class APIManager:
    def __init__(self, api_choice: str):
        self.api_choice = api_choice
        self.api_key = self.load_api_key(api_choice)

    def load_api_key(self, api_choice: str) -> str:
        """APIキーをロードします。"""
        if api_choice == "claude":
            return os.getenv("CLAUDE_API_KEY")
        elif api_choice == "gpt":
            return os.getenv("OPENAI_API_KEY")
        else:
            raise ValueError(f"サポートされていないAPIの選択: {api_choice}")

    def request_review(
        self, full_content: str, changed_content: str, review_point: str
    ) -> str:
        """APIに基づいてレビューをリクエストします。"""
        if self.api_choice == "claude":
            return request_review_claude(
                full_content, changed_content, self.api_key, review_point
            )
        elif self.api_choice == "gpt":
            return request_review_gpt(
                full_content, changed_content, self.api_key, review_point
            )
        else:
            raise ValueError(f"サポートされていないAPIの選択: {self.api_choice}")
