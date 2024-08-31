from typing import Dict, List, Optional

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from .prompt_template import parser, prompt_template

load_dotenv()


class ReviewAPIManager:
    def __init__(self, api_choice: str):
        self.api_choice = api_choice

    def get_model(self) -> str:
        """APIキーをロードします。"""
        if self.api_choice == "openai":
            return ChatOpenAI(model="gpt-4o", temperature=0.1)
        elif self.api_choice == "anthropic":
            return ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1)
        else:
            raise ValueError(f"サポートされていないAPIの選択: {self.api_choice}")

    def request_review(
        self,
        file_contents: str,
        file_changes: str,
        commit_message: str,
        review_point: Optional[str] = None,
    ) -> Dict[str, str | List[str]]:
        """APIに基づいてレビューをリクエストします。"""
        model = self.get_model()
        chain = prompt_template | model | parser
        return chain.invoke(
            {
                "file_contents": file_contents,
                "file_changes": file_changes,
                "commit_message": commit_message,
                "review_point": review_point,
            }
        )
